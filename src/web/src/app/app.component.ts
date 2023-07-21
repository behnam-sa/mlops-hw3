import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Component } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ErrorSnackBarComponent } from './error-snack-bar/error-snack-bar.component';
import { PredictionResult } from './models/prediction-result';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss'],
})
export class AppComponent {
    readonly apiUrl = 'http://localhost:8000/predict' as const;

    loading: boolean = false;
    labelName?: string;
    imageSrc?: string;

    constructor(
        private http: HttpClient,
        private snackBar: MatSnackBar
    ) {}

    readUrl(event: Event): void {
        const files = (event.target as HTMLInputElement)?.files;

        if (files && files[0]) {
            const file = files[0];

            const reader = new FileReader();
            reader.onload = (event) => {
                this.imageSrc = (reader.result as string | null) ?? undefined;

                this.predict(file);
            };

            reader.readAsDataURL(file);
        }
    }

    predict(file: File) {
        const formData = new FormData();
        formData.append('image', file);

        this.loading = true;
        this.labelName = undefined;
        this.http.post<PredictionResult>(this.apiUrl, formData).subscribe({
            next: ({ labelName }) => {
                this.labelName = labelName;
                this.loading = false;
            },
            error: (err) => {
                if (err instanceof HttpErrorResponse) {
                    this.snackBar.openFromComponent(ErrorSnackBarComponent, {
                        data: {
                            message: err.message,
                        },
                    });
                }
                this.loading = false;
                console.error(err);
            },
        });
    }
}
