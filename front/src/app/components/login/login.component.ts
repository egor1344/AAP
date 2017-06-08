import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../service/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  username: String;
  password: String;
  email: String;

  constructor(
    private authService: AuthService,
    private router: Router
    ) { }

  ngOnInit() {
  }

  onLoginSubmit() {

    const user = {
      username: this.username,
      password: this.password,
      email: this.email
    };

    this.authService.authenticateUser(user).subscribe(data => {
      if(data.key){
        console.log(data);
        this.authService.storeUserData(data.key, user.username);
        this.router.navigate(['/']);
      } else {
        this.router.navigate(['login'])
      }
    });

  }

}
