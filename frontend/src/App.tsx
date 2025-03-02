import "./App.css";
import {CalendarDiv} from "@/components/CalendarDiv.tsx";
import {Header} from "@/components/Header.tsx";
import {useEffect, useState} from "react";
import {University} from "../types/University.ts";

function App() {

    const [data, setData] = useState<University | null>(null);

    useEffect(() => {
        fetch("/plan.json")
            .then((res) => res.json())
            .then((json: University) => setData(json))
    }, []);

    return (
        <div className="bg-neutral-800 text-neutral-100 h-screen w-screen p-4">
            <div className="flex flex-row">
                <CalendarDiv/>
                <Header/>
            </div>
            <div>
                {data && Object.keys(data).map((wydzial) => (
                    <div>{wydzial}</div>
                ))}
            </div>
        </div>
    );
}

export default App;

