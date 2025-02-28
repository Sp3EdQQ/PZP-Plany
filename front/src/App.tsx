import "./App.css"
import { useState } from "react"
import { Calendar } from "@/components/ui/calendar"


function App() {

  const [date, setDate] = useState<Date | undefined>(new Date())

  return <div className="bg-neutral-800 text-neutral-100 h-screen w-screen">
    <div className="text-center p-5"> Plany UBB
    </div>
    <Calendar
      mode="single"
      selected={date}
      onSelect={setDate}
      className="rounded-md border"
    />
  </div>
}

export default App
