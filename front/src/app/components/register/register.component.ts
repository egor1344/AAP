import { Component, OnInit, DoCheck } from '@angular/core';
import { Router }                     from '@angular/router';

import { AuthService }       from '../../service/auth.service';
import { ValidationService } from '../../service/validation.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements DoCheck {

  username: String;
  password1: String;
  password2: String;
  email: String;

  usernameIsValid: boolean;
  emailIsValid: boolean = true;
  passIsValid: boolean;

  constructor(
    private authService: AuthService,
    private validate: ValidationService,
    private router: Router
  ) { }

  ngDoCheck() {
    this.usernameIsValid = this.validate.validateLogin(String(this.username));
    // console.log(this.usernameIsValid);
    this.emailIsValid = this.validate.validateEmail(String(this.email));
    let message: string;
    // console.log(this.emailIsValid);
    this.passIsValid = this.validate.validatePass(String(this.password1), String(this.password2));
    console.log(this.passIsValid);
  }

  onRegisterSubmit(){

    const user = {
      username: this.username,
      password1: this.password1,
      password2: this.password2,
      email: this.email
    };

    this.authService.registerUser(user).subscribe(data => {
      if(data.key){
        this.authService.storeUserData(data.key, user.username);
        this.router.navigate(['/']);
      } else {
        return false;
      }
    });

  }

}
