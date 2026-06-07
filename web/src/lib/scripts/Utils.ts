export function capitalize(str: string) {
    return str.split(" ")
        .map((word: string) =>word ? word[0].toUpperCase() + word.slice(1).toLowerCase() : "")
        .join(" ");
}


export function walkDict(obj: any, prefix = ""): {key: string, type: string, value: string}[] {
    let out: {key: string, type: string, value: string}[] = [];

    for (const [k, v] of Object.entries(obj)) {
        if (v && typeof v === "object" && !Array.isArray(v)) {
            out = out.concat(walkDict(v, `${prefix}${k}.`));
        } else {
            out.push({
                key: `${prefix}${k}`,
                type: typeof(v),
                value: `${v}`
            });
        }
    }

    return out;
}

export function toDate(date: Date): string {
    const months = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ];

    const day = date.getDate();
    const month = months[date.getMonth()];
    const year = date.getFullYear();



    return `${day} ${month}, ${year}`;
}

export function emptyArr(length: number): null[] {
    let arr: null[] = [];

    for (let i = 0; i < length; i++) {
        arr.push(null)
    }

    console.log(arr)
    return arr
}  