export let loginForm=`<div class="limiter">
                        <div class="container-login">
                            <form class="login-form validate-form" method="POST" onsubmit="loginRequest(event);">
                                <span class="login-form-title">
                                    LOGIN<i class="fas fa-utensils"></i>
                                </span>
                                <div class="wrap-input validate-input" data-validate = "Username is required">
                                    <input class="input user-name" type="text" name="username" placeholder="Username">
                                    <span class="focus-input"></span>
                                    <span class="symbol-input">
                                        <i class="fa fa-envelope" aria-hidden="true"></i>
                                    </span>
                                </div><br/>
                                <div class="wrap-input validate-input" data-validate = "Password is required">
                                    <input class="input password" type="password" name="password" placeholder="Password">
                                    <span class="focus-input"></span>
                                    <span class="symbol-input">
                                        <i class="fa fa-lock" aria-hidden="true"></i>
                                    </span>
                                </div>
                                <div class="container-login-form-btn">
                                    <button class="favorite styled" type="button">
                                        Clear
                                    </button>
                                    <button class="favorite styled" type="submit">
                                        Enter
                                    </button>
                                </div>
                                <div class="text-center">
                                    <span class="txt1">
                                        Forgot
                                    </span>
                                    <a class="txt2" href="#">
                                        Username / Password?
                                    </a>
                                </div>
                                <div class="text-center">
                                    <a class="txt2" href="/signup/">
                                        Create your Account
                                        <i class="fa fa-long-arrow-right m-l-5" aria-hidden="true"></i>
                                    </a>
                                </div>
                            </form>
                        </div>
                    </div>`

let signupForm=``