import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatButton, MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { AuthService } from '../../services/auth.service';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-signup',
  imports: [MatFormFieldModule, ReactiveFormsModule, FormsModule, MatInputModule, CommonModule, MatButtonModule, RouterModule],

  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.scss']
})
export class SignupComponent {
  username = '';
  email = '';
  password = '';
  error = '';

  constructor(private authService: AuthService, private router: Router) { }

  signup() {
    this.authService.signup(this.username, this.email, this.password).subscribe({
      next: () => this.router.navigate(['/dream']),
      error: (err) => this.error = err.error.error || 'Signup failed'
    });
  }
}