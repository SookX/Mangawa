import { useContext, useEffect, useState } from "react"
import { DataContext } from "../../context/DataContext"

const Dashboard = () => {
    // Gets global data from the context
    const { crud } = useContext(DataContext)



    // Gets the progress from the backend on init
    useEffect(() => {
        const fetchProgress = async () => {
            const response = await crud({
                url: "/progress/",
                method: "get"
            })

            console.log(response)
        }

        fetchProgress()
    }, [])



    // Holds the data form the form
    const [weight, setWeight] = useState(65)
    const [height, setHeight] = useState(180)



    return (
        <form>
            <input
                type="file"
            />
            <input 
                type="number"
                value={weight}
                onChange={(e) => setWeight(e.target.value)}
                placeholder="Weight"
            />
            <input 
                type="number"
                value={height}
                onChange={(e) => setHeight(e.target.value)}
                placeholder="Height"
            />
            <button className="btn" type="submit">Upload</button>
        </form>
    )
}

export default Dashboard