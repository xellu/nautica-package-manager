<script lang="ts">
    import Markdown from "$lib/components/Markdown.svelte";
    import Embed from "$lib/components/Embed.svelte";

    import { toaster } from "$lib/scripts/Toaster";

    import type { Package } from "$lib/types/Package";
    import { onMount } from "svelte";

    import { Account, type AccountType } from "$lib/scripts/Auth.js";

    let User: AccountType | null = $state(null);
    Account.subscribe((value) => { User = value })

    let { data } = $props();
    let packages: Package[] = $derived(
        [...(data.packages ?? [])].sort((a, b) => {
            const latestA = Math.max(...a.versions.map(v => v.createdAt), 0);
            const latestB = Math.max(...b.versions.map(v => v.createdAt), 0);
            return latestB - latestA;
        })
    );
    let error: any = $derived(data.error);

    onMount(async () => {
        if (error != null) {
            toaster.error({description: error})
        }

        // console.log(packages)
    })
</script>

<svelte:head>
    <Embed
        title = "My Packages | Dashboard"
    
    />
</svelte:head>

<div class="flex flex-col gap-5">
    {#each packages as p}
        <div class="card preset-filled-surface-100-900 p-3">
            <div class="flex justify-between">
                <div class="flex items-center gap-1">
                    <p class="font-semibold text-lg mr-2">{p.displayName}</p>
                    <span class="chip font-semibold preset-filled">v{p.versions[p.versions.length-1].id}</span>
                    <span class="chip font-semibold {p.owner == User?.userId ? 'preset-filled-secondary-500' : 'preset-filled-tertiary-500'}">{p.owner == User?.userId ? 'Owner' : 'Maintainer'}</span>
                </div>

                
                <div class="flex items-center max-md:hidden">
                    <a href="/packages/{p.name}"><button class="btn preset-outlined-primary-500 py-1">View</button></a>
                    <a href="/packages/{p.name}/edit"><button class="btn preset-filled-primary-500 py-1.25">Edit</button></a>
                </div>

            </div>
            <p class="mt-1 mb-5 text-xs opacity-75 font-mono">{p.versions.length} releases • {p.maintainers.length+1} maintainers</p>

            {#if p.brief}
                <p class="italic text-surface-800-200">{p.brief}</p>
            {:else}
                <a href="/packages/{p.name}/edit" class="font-mono underline">Add a description to help others find your package {'->'}</a>
            {/if}

            <div class="flex items-center md:hidden max-md:mt-5">
                <a href="/packages/{p.name}" class="grow"><button class="btn btn-sm preset-outlined-primary-500 py-1 w-full">View</button></a>
                <a href="/packages/{p.name}/edit" class="grow"><button class="btn btn-sm preset-filled-primary-500 py-1.25 w-full">Edit</button></a>
            </div>

        </div>
    {/each}

    <!-- publishing guide -->
    {#if packages.length == 0}
        <h2 class="h2">Nothing to show here</h2>
        <p class="mb-32">Packages you publish will show up here</p>

        <!-- i cba to do this properly -->
        <Markdown content = {`
## Creating Packages
A Nautica package is a self-contained service you can publish to the registry and install into any Nautica project.

To create a new package:
\`\`\`bash
nautica package create myservice # the name has to be unique
\`\`\`

This generates a project structure with \`__init__.py\` as the entry point and \`project.n3\` for metadata:
\`\`\`toml
# a-z0-9._- only, must be unique on the registry
name = "myservice"

# follows semver — bump this before every publish
version = "1.0.0"

# other Nautica packages this service depends on
dependsOn = []

# PyPI packages this service depends on
pyPackages = []
\`\`\`

_Your package can have multiple files. \`__init__.py\` & \`project.n3\` in the project's root are the only requirements._

***

## Testing
Nautica tests your service in a real runtime environment rather than with unit tests. It creates a full Nautica project and injects your package as a plugin, so you'll be testing in production environment.

Create the test environment:
\`\`\`bash
nautica package env
\`\`\`

And run the test:
\`\`\`bash
nautica package test
# This will copy your project into the environments \`plugin/\` directory
\`\`\`

Run \`nautica package\` for list of all available commands

***

## Publishing
Before publishing, make sure the \`version\` field in \`project.n3\` is updated. Publishing the same version twice will fail.

\`\`\`bash
nautica package publish
\`\`\`


Your package will be available on
${window.location.protocol}//${window.location.host}/packages/your-package-name

_You may be prompted to sign into your NPR account._
        `} />
    {/if}
</div>
