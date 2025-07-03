import style from './Navbar.module.css';

function Navbar(){
return(
    <>
     <div className={style.navbar}>
        <div className={style.navbarLogo}>
            <h1>Carro Remoto</h1>
        </div>
    </div>
    </>
)
}

export default Navbar