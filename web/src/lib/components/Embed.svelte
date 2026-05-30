<script lang="ts">
    interface Props {
        title?: string | null;
        description?: string | null;
        siteName?: string | null;
        icon?: "default" | "custom" | "customLarge" | "video" | "none";
        iconUrl?: string;
        route?: string;
        color?: string;
        disable?: boolean;
    }

    let {
        title = null,
        description = null,
        siteName = "xellu.xyz",
        icon = "default",
        iconUrl = "",
        route = "/",
        color = "#45a6ff",
        disable = false,
    }: Props = $props();
</script>

{#if !disable}
    <meta name="author" content="Xellu" />
    <meta name="description" content="Package registry for Nautica API" />
    <meta name="keywords" content="Nautica API, Nautica Package Manager, NAPM, NAPI, Nautica3 Package Manager, Nautica Package Registry, Nautica Packages" />

    <meta name="title" content="{title}" />

    <meta property="og:url" content="https://xellu.xyz{route}" />
    <meta property="og:type" content="website" />

    <meta content="{color}" data-react-helmet="true" name="theme-color" />
{/if}

{#if title}
    <meta property="og:title" content="{title}" />
    <title>{title}</title>    
{/if}
{#if description} <meta property="og:description" content="{description}" /> {/if}
{#if siteName} <meta property="og:site_name" content="{siteName}" /> {/if}

{#if icon == "default"}
    <meta property="og:image" content="/favicon.png" />

{:else if icon == "custom"}
    <meta property="og:image" content="{iconUrl}" />

{:else if icon == "customLarge"}
    <meta property="og:image" content="{iconUrl}" />
    <meta name="twitter:card" content="summary_large_image">
{:else if icon == "video"}
    <meta property="og:image" content="{iconUrl}" />
    <meta property="og:image:type" content="video/mp4" />
    <meta property="og:image:width" content="1280" />
    <meta property="og:image:height" content="720" />
{/if}