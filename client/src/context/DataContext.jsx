import axios from "axios";
import { createContext, useState } from "react";
import { useNavigate } from "react-router-dom";

export const DataContext = createContext({ })

const DataProvider = ({ children }) => {
    // Sends the user to a different page
    const navigate = useNavigate()



    // Gets the JWT tokens if the user has logged in
    const [refresh, setRefresh] = useState(localStorage.getItem('refresh') || null)
    const [access, setAccess] = useState(localStorage.getItem('access') || null)



    // Sets the url for the backend server
    axios.defaults.baseURL = 'http://127.0.0.1:8000/'



    // Makes a CRUD operation to the backend server
    const crud = async ({ url, method, body = null, headers = null }) => {
        try {
            const config = {
                headers: access ? {
                    'Authorization': `Bearer ${access}`,
                    ...headers
                } : {
                    headers
                }
            }

            let response;
            if (method.toLowerCase() === 'get' || method.toLowerCase() === 'delete') {
                response = await axios[method](url, config);
            } else {
                response = await axios[method](url, body, config);
            }

            if(response) return response
        } catch(err) {
            return err
        }
    }



    // Holds whether the layout grid is shown or not
    const [grid, setGrid] = useState(false)



    return (
        <DataContext.Provider value={{
            navigate,
            crud, access, setAccess, refresh, setRefresh,
            grid, setGrid
        }}>
            { children }
        </DataContext.Provider>
    )
}

export default DataProvider