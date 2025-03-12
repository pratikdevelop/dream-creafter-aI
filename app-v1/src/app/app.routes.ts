import { Routes } from '@angular/router';
import { DreamInputComponent } from './components/dream-input/dream-input.component';
import { LoginComponent } from './components/login/login.component';
import { SignupComponent } from './components/signup/signup.component';
import { DreamHistoryComponent } from './components/dream-display/dream-history.component';

export const routes: Routes = [
    { path: 'signup', component: SignupComponent },
    { path: 'login', component: LoginComponent },
    { path: 'dream', component: DreamInputComponent },
    { path: '', redirectTo: '/login', pathMatch: 'full' },
    { path: 'history', component: DreamHistoryComponent },
];
