import httpx
import logging
from typing import Dict, List, Any, Optional
from app.models.device import Device

logger = logging.getLogger(__name__)


class F5Manager:
    def __init__(self, device: Device):
        self.host = device.ip_address
        self.port = device.port or 443
        self.username = device.username
        self.password = device.password
        self.base_url = f"https://{self.host}:{self.port}/mgmt/tm"
        self.verify_ssl = False

    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        async with httpx.AsyncClient(
            verify=self.verify_ssl,
            timeout=15,
            auth=(self.username, self.password),
            follow_redirects=True
        ) as client:
            try:
                response = await client.request(method, url, **kwargs)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                logger.error(f"F5 API request failed: {e}")
                raise
            except Exception as e:
                logger.error(f"F5 request exception: {e}")
                raise

    async def test_connection(self) -> Dict[str, Any]:
        try:
            response = await self._make_request("GET", "/sys/version")
            return {
                "success": True,
                "version": response.get("version", ""),
                "build": response.get("build", ""),
                "message": "设备连接成功"
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }

    async def get_device_info(self) -> Dict[str, Any]:
        result = await self._make_request("GET", "/sys/version")
        return {
            "hostname": result.get("hostname", ""),
            "version": result.get("version", ""),
            "build": result.get("build", ""),
            "edition": result.get("edition", "")
        }

    async def get_virtual_servers(self) -> List[Dict[str, Any]]:
        try:
            response = await self._make_request("GET", "/ltm/virtual")
            items = response.get("items", [])
            return [
                {
                    "name": item.get("name", ""),
                    "address": item.get("destination", "").replace("/Common/", ""),
                    "status": item.get("status", {}).get("availabilityStatus", "unknown"),
                    "enabled": item.get("enabled", True),
                    "description": item.get("description", "")
                }
                for item in items
            ]
        except Exception as e:
            logger.error(f"Failed to get virtual servers: {e}")
            return []

    async def get_pools(self) -> List[Dict[str, Any]]:
        try:
            response = await self._make_request("GET", "/ltm/pool")
            items = response.get("items", [])
            pools = []
            for item in items:
                members = []
                if "membersReference" in item:
                    members_url = item["membersReference"]["link"].replace(
                        "https://localhost/mgmt", self.base_url
                    )
                    try:
                        members_response = await self._make_request("GET", members_url.replace(self.base_url, ""))
                        members = [
                            {
                                "name": m.get("name", ""),
                                "address": m.get("address", ""),
                                "status": m.get("status", {}).get("availabilityStatus", "unknown")
                            }
                            for m in members_response.get("items", [])
                        ]
                    except Exception:
                        pass
                pools.append({
                    "name": item.get("name", ""),
                    "status": item.get("status", {}).get("availabilityStatus", "unknown"),
                    "members": members,
                    "description": item.get("description", "")
                })
            return pools
        except Exception as e:
            logger.error(f"Failed to get pools: {e}")
            return []

    async def get_nodes(self) -> List[Dict[str, Any]]:
        try:
            response = await self._make_request("GET", "/ltm/node")
            items = response.get("items", [])
            return [
                {
                    "name": item.get("name", ""),
                    "address": item.get("address", ""),
                    "status": item.get("status", {}).get("availabilityStatus", "unknown"),
                    "enabled": item.get("enabled", True)
                }
                for item in items
            ]
        except Exception as e:
            logger.error(f"Failed to get nodes: {e}")
            return []

    async def get_certificates(self) -> List[Dict[str, Any]]:
        try:
            response = await self._make_request("GET", "/sys/crypto/cert")
            items = response.get("items", [])
            return [
                {
                    "name": item.get("name", ""),
                    "commonName": item.get("commonName", ""),
                    "serialNumber": item.get("serialNumber", ""),
                    "expirationDate": item.get("expirationDate", ""),
                    "issuer": item.get("issuer", "")
                }
                for item in items
            ]
        except Exception as e:
            logger.error(f"Failed to get certificates: {e}")
            return []

    async def get_device_status(self) -> Dict[str, Any]:
        try:
            version_info = await self.get_device_info()
            cpu_response = await self._make_request("GET", "/sys/performance/stats")
            cpu_usage = cpu_response.get("entries", {}).get("https://localhost/mgmt/tm/sys/performance/stats/cpu", {}).get("nestedStats", {}).get("entries", {})
            
            return {
                "online": True,
                "version": version_info.get("version", ""),
                "hostname": version_info.get("hostname", ""),
                "cpu": {
                    "user": cpu_usage.get("user", {}).get("value", 0),
                    "system": cpu_usage.get("system", {}).get("value", 0),
                    "idle": cpu_usage.get("idle", {}).get("value", 0)
                },
                "memory": {
                    "total": cpu_response.get("memoryTotal", 0),
                    "used": cpu_response.get("memoryUsed", 0)
                }
            }
        except Exception as e:
            return {
                "online": False,
                "message": str(e)
            }

    async def get_traffic_stats(self) -> Dict[str, Any]:
        try:
            response = await self._make_request("GET", "/ltm/traffic/stats")
            return {
                "entries": response.get("entries", {})
            }
        except Exception as e:
            logger.error(f"Failed to get traffic stats: {e}")
            return {"entries": {}}


async def discover_device(device: Device) -> Dict[str, Any]:
    f5 = F5Manager(device)
    result = await f5.test_connection()
    
    if not result["success"]:
        return result
    
    info = await f5.get_device_info()
    return {
        "success": True,
        "message": "设备纳管成功",
        "version": info.get("version", ""),
        "hostname": info.get("hostname", ""),
        "build": info.get("build", ""),
        "edition": info.get("edition", "")
    }


async def sync_device_config(device: Device) -> Dict[str, Any]:
    f5 = F5Manager(device)
    try:
        virtual_servers = await f5.get_virtual_servers()
        pools = await f5.get_pools()
        nodes = await f5.get_nodes()
        certificates = await f5.get_certificates()
        
        return {
            "success": True,
            "message": "配置同步成功",
            "virtual_servers": len(virtual_servers),
            "pools": len(pools),
            "nodes": len(nodes),
            "certificates": len(certificates)
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }