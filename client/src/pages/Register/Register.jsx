import { useContext, useEffect, useState } from "react"
import { DataContext } from "../../context/DataContext"

const Register = () => {
    // Gets global data from the context
    const { crud, navigate, access } = useContext(DataContext)



    // Checks if the user has already logged in
    useEffect(() => {
        if(access) navigate('/dashboard')
    }, [access])



    // Stores the data for the form
    const [username, setUsername] = useState('')
    const [first_name, setFirstName] = useState('')
    const [last_name, setLastName] = useState('')
    const [email, setEmail] = useState('')
    const [age, setAge] = useState(18)
    const [gender, setGender] = useState('Male')
    const [password, setPassword] = useState('')



    // Stores the state for the form
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)



    // Makes a register request to the backend
    const handleSubmit = async (e) => {
        e.preventDefault()

        setLoading(true)

        const response = await crud({
            url: '/user/register/',
            method: 'post',
            body: {
                username,
                first_name,
                last_name,
                email,
                password,
                age,
                gender
            }
        })

        console.log(response)

        if(response.status == 201) navigate('/login')
        else setError(response.data.error)

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
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username"
            />
            <input
                type="text"
                value={first_name}
                onChange={(e) => setFirstName(e.target.value)}
                placeholder="First Name"
            />
            <input
                type="text"
                value={last_name}
                onChange={(e) => setLastName(e.target.value)}
                placeholder="Last Name"
            />
            <input
                type="text"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Email"
            />
            <input
                type="number"
                value={age}
                onChange={(e) => setAge(e.target.value)}
                placeholder="Age"
            />
            <select value={gender} onChange={(e) => setGender(e.target.value)}>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
            </select>
            <input
                type="text"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
            />

            <button className="btn" type="submit">Register</button>
        </form>
    )
}

export default Register