import { Component, OnInit, DoCheck } from '@angular/core';
import { AuthService }       from '../../service/auth.service';
import { Router }            from '@angular/router';

@Component({
  selector: 'app-nav-bar',
  templateUrl: './nav-bar.component.html',
  styleUrls: ['./nav-bar.component.css']
})
export class NavBarComponent implements OnInit, DoCheck {

  login: boolean;

  constructor(
    private authService: AuthService,
    private router: Router
  ) { }

  ngDoCheck() {
    if (this.authService.isLogin()) {
        this.login = true;
    } else {
      this.login = false;
    }
    console.log(this.login);
  }

  ngOnInit() {
    if (this.authService.isLogin()) {
        this.login = true;
    } else {
      this.login = false;
    }
    console.log(this.login);
  }

  onLogoutClick(){
    this.authService.logout();
    this.router.navigate(['/login']);
    this.login = false;
    return false;
  }

}
