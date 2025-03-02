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
        <div className="bg-neutral-800 text-neutral-100 h-max w-screen p-4">
            <div className="flex flex-row">
                <CalendarDiv/>
                <Header/>
            </div>
            {data && Object.entries(data).map(([facultyName, faculty]) => (

                <div key={facultyName} className="mb-6">
                    <div className="text-2xl font-semibold">{facultyName}</div>

                    {Object.entries(faculty).map(([departmentName, department]) => (

                        <div key={departmentName} className="ml-4">
                            <div className="text-xl mt-2">{departmentName}</div>

                            {Object.entries(department).map(([subject, lecturers]) => (
                                <div key={subject} className="ml-6">
                                    <p className="text-xl">{subject}:</p>
                                    <ul className="list-disc list-inside">

                                        {lecturers.map((lecturer, index) => (
                                            <li key={index}>{lecturer}</li>
                                        ))
                                        }

                                    </ul>
                                </div>
                            ))
                            }
                        </div>

                    ))
                    }
                </div>

            ))
            }
        </div>
    );
}

export default App;

