import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { RouterModule, Routes } from '@angular/router';

import { AppComponent } from './app.component';
import { NavBarComponent } from './components/nav-bar/nav-bar.component';
import { HomeComponent } from './components/home/home.component';
import { ApartListComponent } from './components/apart-list/apart-list.component';
import { ApartDetailComponent } from './components/apart-detail/apart-detail.component';
import { StatisticaComponent } from './components/statistica/statistica.component';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';

import { ApartmentService } from './service/apartment.service';
import { AuthService } from './service/auth.service';

const appRoutes: Routes = [
  {path:'', component:HomeComponent},
  {path:'apartment', component:ApartListComponent},
  {path:'detail/:id', component:ApartDetailComponent},
  {path:'login', component:LoginComponent},
  {path:'register', component:RegisterComponent},

]

@NgModule({
  declarations: [
    AppComponent,
    NavBarComponent,
    HomeComponent,
    ApartListComponent,
    ApartDetailComponent,
    StatisticaComponent,
    LoginComponent,
    RegisterComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    RouterModule.forRoot(appRoutes)
  ],
  providers: [ApartmentService, AuthService],
  bootstrap: [AppComponent]
})
export class AppModule { }
