export type PackageVersion = {
    id: string,
    file: string,
    author: string,
    createdAt: number
}

export type Package = {
    name: string,
    versions: PackageVersion[],
    installs: number,

    displayName: string,
    brief: string,
    readMe?: string,

    owner: string,
    ownerExpanded?: {username: string, id: string},
    maintainers: string[],
    maintainersExpanded?: {username: string, id: string}[],
    
}