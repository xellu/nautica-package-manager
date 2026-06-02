export type PackageVersion = {
    id: string,
    fileUrl: string,
    author: string,
    createdAt: number
}

export type Package = {
    name: string,
    versions: PackageVersion[],

    displayName: string,
    brief: string,

    owner: string,
    maintainers: string[]
}