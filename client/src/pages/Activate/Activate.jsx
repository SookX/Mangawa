import { useContext, useEffect } from "react"
import { useParams } from "react-router-dom"
import { DataContext } from "../../context/DataContext"

const Activate = () => {
    // Gets global data from the context
    const { crud, navigate } = useContext(DataContext)



    // Gets parameters from the url
    const uidb64 = useParams().uidb64
    const token = useParams().token



    // Makes an activation request to the backend
    useEffect(() => {
        const activate = async () => {
            const response = await crud({
                url: `/user/activate/${uidb64}/${token}/`,
                method: 'get'
            })

            console.log(response)

            if(response.status == 200) navigate('/login')
        }


        if(uidb64 && token) activate()
    }, [uidb64, token])



    return (
        <>
            <p>Activating your account...</p>
            <p>UIDB: {uidb64}</p>
            <p>token: {token}</p>
        </>
    )
}

export default Activate