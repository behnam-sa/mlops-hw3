import { Component, Inject } from '@angular/core';
import {
    MAT_SNACK_BAR_DATA,
    MatSnackBarRef,
} from '@angular/material/snack-bar';

@Component({
    selector: 'app-error-snack-bar',
    templateUrl: './error-snack-bar.component.html',
    styleUrls: ['./error-snack-bar.component.scss'],
})
export class ErrorSnackBarComponent {
    constructor(
        @Inject(MAT_SNACK_BAR_DATA) public data: { message: string },
        public snackBarRef: MatSnackBarRef<ErrorSnackBarComponent>
    ) {}
}
