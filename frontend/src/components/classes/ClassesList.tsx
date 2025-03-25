type ClassesListProps = {
    groupedBySubject: Record<string, Record<string, { rooms: string[] }>>;
    selectedType: string | null;
};

export const ClassesList = ({groupedBySubject, selectedType}: ClassesListProps) => {
    if (!selectedType || Object.keys(groupedBySubject).length === 0) {
        return <p className="text-center text-gray-500">Brak zajęć dla wybranego trybu lub grupy.</p>;
    }

    return (
        <div className="grid grid-cols-2 gap-6">
            {Object.entries(groupedBySubject).map(([subject, teachers]) => (
                <div key={subject} className="card">
                    <h2 className="title">{subject}</h2>
                    <ul className="space-y-2">
                        {Object.entries(teachers).map(([nauczyciel, {rooms}], index) => (
                            <li key={index} className="text-center">
                                <p className="font-semibold">{nauczyciel}</p>
                                <p className="text-sm text-gray-600">Sala: {rooms.join(", ")}</p>
                            </li>
                        ))}
                    </ul>
                </div>
            ))}
        </div>
    );
};
