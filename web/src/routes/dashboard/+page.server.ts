import type { PageServerLoad } from "./$types";
import { API_URL } from "$lib/Config";
import type { Package } from "$lib/types/Package";

export const load: PageServerLoad = async ({ cookies }) => {
    const session = cookies.get("session");
    if (!session) return { packages: [] };

    const r = await fetch(`${API_URL}/account/packages`, {
        headers: { Cookie: `session=${session}` }
    });

    let error: string | null = null;
    let packages: Package[] = [];

    let data: any;
    if (!r.ok) {
        try {
            data = await r.json();
            error = data.error || "Unknown Error"
        } catch(e) {
            error = `${e}`
        }
    } else {
        data = await r.json();
        packages = data;
    }

    return { packages, error };
};
