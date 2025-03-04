import {useState} from "react";
import {University} from "../../types/University.ts";

type ZajeciaProps = {
    propCatedral: string;
    propSelectedWydzial: string;
    propData: University;
}

export const Zajecia = ({propCatedral, propSelectedWydzial, propData}: ZajeciaProps) => {
    const [showClasses, setShowClasses] = useState(false);
    const zajecia = propData[propSelectedWydzial]?.[propCatedral] || {};

    return (
        <div className="my-4">
            <div
                className="bg-blue-500 p-3 cursor-pointer rounded-lg text-lg"
                onClick={() => setShowClasses(!showClasses)}
            >
                {propCatedral}
            </div>
            {showClasses && (
                <div className="grid grid-cols-1 gap-4 mt-3">
                    {Object.entries(zajecia).map(([nazwaZajec, nauczyciele]) => (
                        <div key={nazwaZajec} className="bg-blue-500 p-4 rounded-lg shadow-lg">
                            <h2 className="text-xl font-bold border-b pb-2 mb-2">{nazwaZajec}</h2>
                            <ul>
                                {nauczyciele.map((nauczyciel, index) => (
                                    <li key={index} className="text-sm">{nauczyciel}</li>
                                ))}
                            </ul>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};
