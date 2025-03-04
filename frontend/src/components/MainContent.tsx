import {Zajecia} from "@/components/Zajecia.tsx";
import {University} from "../../types/University.ts";

type MainContentProps = {
    propSelectedWydzial: string;
    propData: University;
}

export const MainContent = ({propSelectedWydzial, propData}: MainContentProps) => {

    const faculty = propData[propSelectedWydzial];
    return (
        <div className="w-4/5 p-5 overflow-x-hidden">
            <h1 className="text-center p-5 text-5xl">Plany UBB</h1>
            <div>
                <h1 className="text-center font-bold text-lg ">{propSelectedWydzial}</h1>
                {faculty ? (
                    Object.keys(faculty).map((catedral) => (
                        <Zajecia
                            key={catedral}
                            propCatedral={catedral}
                            propSelectedWydzial={propSelectedWydzial}
                            propData={propData}
                        />
                    ))
                ) : (
                    <div>
                        <div>Witaj na stronie Plany UBB</div>
                        <div>Kliknij po lewej stronie na wydział aby wyszukać katedry.</div>
                    </div>
                )}
            </div>
        </div>
    );
};
