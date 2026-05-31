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
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];

    const day = date.getDate();
    const month = months[date.getMonth()];
    const year = date.getFullYear();

    const suffix =
        day % 100 >= 11 && day % 100 <= 13
            ? "th"
            : day % 10 === 1
                ? "st"
                : day % 10 === 2
                    ? "nd"
                    : day % 10 === 3
                        ? "rd"
                        : "th";

    return `${day}${suffix} of ${month}, ${year}`;
}
