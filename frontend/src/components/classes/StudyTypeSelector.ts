export const getStudyTypes = () => ["S", "NZ", "NW"];

export const getStudyTypeLabel = (type: string) => {
    switch (type) {
        case "S":
            return "Stacjonarne";
        case "NZ":
            return "Zaoczne";
        case "NW":
            return "Wieczorowe";
        default:
            return "Nieznany";
    }
};
