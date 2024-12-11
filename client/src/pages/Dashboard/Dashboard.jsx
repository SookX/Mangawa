import { useContext, useEffect, useState } from "react"
import { DataContext } from "../../context/DataContext"

const Dashboard = () => {
    // Gets global data from the context
    const { crud, access } = useContext(DataContext)



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
    const [image, setImage] = useState(null)
    const [weight, setWeight] = useState(65)
    const [height, setHeight] = useState(180)



    // Appends the file to the form data
    const handleFileAppend = (e) => {
        if(e.target.files[0]) {
            setImage(e.target.files[0])
        }
    }



    // Makes a request to the backend with the progress
    const handleSubmit = async (e) => {
        e.preventDefault()

        const formData = new FormData()
        formData.append("image", image)
        formData.append("weight", weight)
        formData.append("height", height)

        console.log(image)

        console.log(formData)

        const response = await crud({
            url: '/progress/',
            method: 'post',
            body: formData
        })

        // try {
            
        //     const config = {
        //         headers: {
        //             'Authorization': `Bearer ${access}`,
        //         }
        //     }

        //     const response = await axios.post('/progress/', formData, config)

        //     console.log(response)
        // } catch(err) {
        //     console.log(err)
        // }

        console.log(response)
    }



    return (
        <form onSubmit={(e) => handleSubmit(e)}>
            <input
                type="file"
                onChange={(e) => handleFileAppend(e)}
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

            {/* <img src="https://res.cloudinary.com/djm6yhqvx/image/upload/media/progress_images/Screenshot_2024-11-27_221606_owrj3y" alt="" /> */}
        </form>
    )
}

export default Dashboard