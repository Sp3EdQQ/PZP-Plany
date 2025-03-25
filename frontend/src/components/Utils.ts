export const getStudyType = (groups: string[]) => {
    if (!groups || groups.length === 0) return "S";
    if (groups.some((g) => g.includes("/NZ/"))) return "NZ";
    if (groups.some((g) => g.includes("/NW/"))) return "NW";
    return "S";
};

export const getGroups = (groups: string[]) => {
    return groups
        .map(g => g.split("/").pop())
        .filter(g => g && /^\d+gr$/.test(g || ""));
};
