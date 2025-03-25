export const getGroups = (groups: string[]): (string | undefined)[] => {
    return groups
        .map(g => g.split("/").pop()) // Pobiera ostatnią część ścieżki (np. "1gr", "2gr")
        .filter(g => g && /^\d+gr$/.test(g || "")); // Filtruje poprawne wartości
};
