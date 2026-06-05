from nautica import Service, Logger
from nautica.ext.Util import rmFile
from nautica.services.builtins.shell.decorator import RegisterCommand, CommandRequirements

import datetime

class PackageAdmin(Service):
    def onStart(self, registry):
        @RegisterCommand(
            "rmpackage", "Delete a package off the registry",
            CommandRequirements(
                args = {"name": str}, flags=["confirm"]
            )
        )
        def delete_package(name: str, confirm: bool = False):
            p = registry["MongoDB"]("packages").find_one({"name": name})
            if not p:
                Logger.error("Package does not exist")
                return
            
            if not confirm:
                Logger.warn("Deleting this package can cause other packages to break, if you're sure proceed with the --confirm flag")
                return
            
            registry["MongoDB"]("packages").delete_one({"name": name})
            for v in p.get("versions", []):
                if v.get("file").startswith("static"):
                    ok, _, _ = rmFile(v.get("file"))
                    if ok: Logger.ok(f"Removed version: {v['id']}")
                    else: Logger.warn(f"Unable to delete version: {v['id']}")
                    
            Logger.ok("Package Deleted")

        @RegisterCommand(
            "rmversion", "Delete a package version off the registry",
            CommandRequirements(
                args = {"name": str, "version": str}
            )
        )
        def delete_version(name: str, version: str):
            p = registry["MongoDB"]("packages").find_one({"name": name})
            if not p:
                Logger.error("Package does not exist")
                return
            
            ver = None
            for v in p.get("versions", []):
                if v.get("id") == version:
                    ver = v
                    break
                
            if not ver:
                Logger.error("Version does not exist")
                return
            
            p["versions"].remove(ver)
            if ver.get("file", "").startswith("static"):
                ok, _, _ = rmFile(ver.get("file"))
                if ok: Logger.ok("Removed from storage")
                else: Logger.error("Failed to remove from storage")
            
            registry["MongoDB"]("packages").update_one({"name": name}, {"$set": {"versions": p["versions"]}})
            Logger.ok("Version deleted")

        @RegisterCommand(
            "lsversion", "List package versions",
            CommandRequirements(args={"name": str})
        )
        def list_versions(name):
            p = registry["MongoDB"]("packages").find_one({"name": name})
            if not p:
                Logger.error("Package does not exist")
                return
            
            table = Logger.table()
            table.labels(["Version ID", "Hash", "File", "Author", "Created Date (DD-MM-YYYY)"])
            for v in p.get("versions", []):
                date = datetime.date.fromtimestamp(v['createdAt'])
                table.row([v['id'], v.get('hash'), v.get('file') or v.get('fileUrl'), v['author'], f"{date.day}-{date.month}-{date.year}"])

            table.display()
        
Service.Export(PackageAdmin, depends_on=["Shell", "MongoDB"])