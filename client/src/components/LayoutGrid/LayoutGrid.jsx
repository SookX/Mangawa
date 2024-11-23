import { useContext, useEffect, useState } from "react"
import { DataContext } from "../../context/DataContext"

const LayoutGrid = ({ type, color = 'rgba(255, 0, 0, 0.1)' }) => {
    // Holds whether or not the layout grid is shown
    const { grid, setGrid } = useContext(DataContext)



    // Hold the properties of the layout grid - padding, gutter and number of columns
    const [padding, setPadding] = useState()
    const [gutter, setGutter] = useState()
    const [columns, setColumns] = useState()



    // Updates the grid properties using the CSS variables for them
    const handleResize = () => {
        if(type === 'screen') {
            let root = getComputedStyle(document.documentElement)

            setPadding(root.getPropertyValue('--grid-padding').trim())
            setGutter(root.getPropertyValue('--grid-gutter').trim())
            setColumns(root.getPropertyValue('--grid-columns').trim())
        }
    }



    // Calls the handleResize() function each time the screen gets resized so the grid can be responsive
    useEffect(() => {
        handleResize()

        window.addEventListener('resize', handleResize)

        return () => window.removeEventListener('resize', handleResize)
    }, [])

    

    return (
        <>
            <div className={`layout-grid ${!grid && 'hidden'}`}>
                {
                    Array.from({ length: columns }, (_, i) => (
                        <div className="grid-column" style={{ 'backgroundColor': color }} key={i}></div>
                    ))
                }
            </div>

            <button className="btn grid-btn" onClick={() => setGrid(!grid)}>Grid</button>
        </>
    )
}

export default LayoutGrid