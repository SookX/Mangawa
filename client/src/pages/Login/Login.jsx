import { useContext, useEffect, useState } from "react"
import { DataContext } from "../../context/DataContext"

const Login = () => {
    // Gets global data from the context
    const { crud, access, setAccess, refresh, setRefresh, navigate } = useContext(DataContext)



    // Checks if the user has already logged in
    useEffect(() => {
        if(access) navigate('/dashboard')
    }, [access])



    // Stores the data for the form
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')



    // Stores the state for the form
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)



    // Makes a login request to the backend
    const handleSubmit = async (e) => {
        e.preventDefault()

        setLoading(true)

        const response = await crud({
            url: '/user/login/',
            method: 'post',
            body: {
                email,
                password
            }
        })

        console.log(response)

        if(response.status == 200) {
            setAccess(response.data.token.access)
            setRefresh(response.data.token.refresh)
            localStorage.setItem('access', response.data.token.access)
            localStorage.setItem('refresh', response.data.token.refresh)
            navigate('/dashboard')
        }
        else setError(response.response.data.error)

        setLoading(false)
    }



    return (
        <form onSubmit={(e) => handleSubmit(e)}>
            {
                error &&
                <p className="error">{error}</p>
            }

            <input
                type="text"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Email"
            />
            <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
            />

            <button className="btn" type="submit">Log in</button>
        </form>
    )
}

export default Login