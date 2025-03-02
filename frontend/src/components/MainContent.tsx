import {University} from "../../types/University.ts";

type MainContentProps = {
    propSelectedWydzial: string;
    propData: University;
}
export const MainContent = ({propSelectedWydzial, propData}: MainContentProps) => {
    const faculty = propData[propSelectedWydzial];

    return (<div className="w-4/5">
        <h1 className="text-center p-5 text-4xl">Plany UBB</h1>
        <div>{propSelectedWydzial}</div>
        <div>
            <h1>{propSelectedWydzial}</h1>
            {faculty ? (
                Object.keys(faculty).map((katedra) => <div key={katedra}>{katedra}</div>)
            ) : (
                <div>Wybierz katedre</div>
            )}
        </div>
    </div>)
}