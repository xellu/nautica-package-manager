import { error } from '@sveltejs/kit';
import { API_URL } from '$lib/Config.js';
import type { PageServerLoad } from './$types.js';

export const load: PageServerLoad = async ({ params }) => {
    const r = await fetch(`${API_URL}/package/page/${params.name}/latest`);
    const data = await r.json();

    if (!r.ok) {
        error(r.status, data.error || 'Unknown Error');
    }

    return { package: data };
};
