import React, {useState, useEffect} from "react";
import { Link, Redirect } from 'react-router-dom';
import DoubleLogo from '../Snippets/DoubleLogo';
import {login} from "../auth";

const Login = (props)=>{
    const [message, setMessage] = useState([]);
    const [identifier, setIdentifier] = useState('');
    const [identifierError, setIdentifierError] = useState(undefined);
    const [password, setPassword] = useState('');
    const [passwordError, setPasswordError] = useState(undefined);
    const [remember, setRemember] = useState(false);
    const [authenticated, setAuthenticated ] =  useState(props.authenticated);

    const LOGIN_URL = "/api/login";
    useEffect(()=>{
        document.title = props.title;
    }, []);
    
    const handleIdentifier = (e)=>{
        setIdentifier(e.target.value);
    }
    const handlePassword = (e)=>{
        setPassword(e.target.value);
    }
    const handleRemember = (e)=>{
        setRemember(e.target.checked);
    }
    const handleSubmit = e =>{
        e.preventDefault();
        if (!identifier){
            setIdentifierError("نمیتواند خالی باشد.");
            return;
        }
        if (!password){
            setPasswordError("نمیتواند خالی باشد.");
            return;
        }
        fetch(LOGIN_URL, {
            method: 'POST', 
            headers: {
              'Content-Type': 'application/json'
            },
           
            body: JSON.stringify({identifier, password, remember}) 
          }).then(response=>{   
              response.json().then(data=>{
                  if (data.access_token){
                      login(data.access_token)
                      setAuthenticated(true);
                  }
                  else{
                    setMessage(data.message)
                  }  
                })
            });
          
    }
    return (
        <div className="container-fluid row p-0" id="login_page">
            {authenticated && <Redirect to="/"/>}
        <div className="col-12 col-md-6  p-4" id="login_form_container">
            <form action="" method="POST" className="w-100" onSubmit={handleSubmit}>
                <fieldset className="form-group ">
                    <legend className="mb-4 text-center">
                        <DoubleLogo />
                    </legend>
                    <div className="inputs px-md-5">
                        <div className="form-group  mb-5 ">
                            <div className="input-group mb-3  bg-none new_design_inputs">
                                <input className="form-control form-control-lg pe-5" name="identifier" placeholder=" " value={identifier} onChange={handleIdentifier}/>
                                <label htmlFor="identifier" className="form-control-label pb-2">شماره دانشجویی</label>
                                <i className="bi-person-fill"></i>
                            </div>
                            { identifierError &&
                                <div class="invalid-feedback ">
                                    identifierError
                                </div>
                            }
                        </div>
                        <div className="form-group my-5 ">
                            
                            
                            <div className="input-group mb-3  bg-none new_design_inputs">
                                <input className="form-control form-control-lg pe-5" name="password" type="password" placeholder=" " value={password} onChange={handlePassword}/>
                                <label htmlFor="password" className="form-control-label pb-2">رمز عبور</label>

                                <i className="bi-shield-lock-fill"></i>
                                
                            </div>
                        </div>
                        <div className="input-group mb-3  bg-none ">
                            <button className="btn btn-main btn-lg w-50 rounded d-flex align-items-center justify-content-center" type="submit">ورود</button>
                            <a className="btn btn-simple  text-center w-50 text-main text-black-75" href="#" >
                                    <small>بازیابی رمز عبور</small>
                            </a>
                        </div>

                        <div className="form-group mt-4">
                        </div>
                        <div className="form-group  mb-5 d-flex   justify-content-between align-items-center  border-top pt-2">
                            <small className="text-muted col-6 text-start ">
                                حساب ندارید؟
                                <Link to="/register"><a className="ms-2 text-main fw-bolder" href="/register">ثبت نام </a></Link>
                            </small>
                                <div className=" col-6  text-end ">
                                    <input className="" name="remember" type="checkbox" checked={remember} onChange={handleRemember}/>
                                    <label htmlFor="password" className="form-control-label ms-2">مرا به خاطر بسپار</label>
                                </div>     
                                            
                        </div>
                    </div>
                </fieldset>
                {message.length>0 && 
                    `
                    <div className="alert alert-${message[1]}" role="alert">
                        ${ message[0] }
                    </div>
                    `
                }
            </form>
        </div>
        <div className="col-12 col-md-6 info px-0 d-flex text-white">
            <div className="pnu_logo h-100 "></div>
            <div className="content p-2  d-flex justify-content-center align-items-start flex-column">
                <h1>PCPC</h1>
                <h5>پنجمین دوره مسابقات برنامه نویسی دانشجویی</h5>
                <h5>دانشگاه های پیام نور کشور - تبریز</h5>
            </div>
        </div>
    </div>
    )
}


export default Login;