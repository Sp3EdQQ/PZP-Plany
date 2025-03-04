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
                className={`bg-blue-700 text-white p-4 cursor-pointer rounded-xl text-lg font-semibold shadow-lg transition duration-300 hover:bg-blue-800 hover:scale-102 ${showClasses ? "bg-blue-800 scale-102" : ""}`}
                onClick={() => setShowClasses(!showClasses)}
            >
                {propCatedral}
            </div>
            {showClasses && (
                <div className="grid grid-cols-1 gap-6 mt-4">
                    {Object.entries(zajecia).map(([nazwaZajec, nauczyciele]) => (
                        <div key={nazwaZajec}
                             className="bg-blue-600 p-6 rounded-xl shadow-md text-white border border-blue-400 hover:bg-blue-700 transition duration-300">
                            <h2 className="text-xl font-bold border-b border-white pb-2 mb-2">{nazwaZajec}</h2>
                            <ul className="space-y-1">
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
