
    // ------ ALMINDELIG QUIZ ------
    function checkAnswers() {
        console.log("checkAnswers() blev kaldt"); // Test
        let score = 0;
        const totalQuestions = 2;

        // Spørgsmål 1 i alm. quiz
        const q1 = document.querySelector('input[name="quiz1_question1"]:checked');
        // Rigtige svar er value="2" (dvs. grad=2)
        if (q1 && q1.value === "2") {
            score++;
        }

        // Spørgsmål 2 i alm. quiz
        const q2 = document.querySelector('input[name="quiz1_question2"]:checked');
        // Rigtige svar er value="3" (dvs. koefficienten er 42)
        if (q2 && q2.value === "3") {
            score++;
        }

        // Vis resultat for alm. quiz
        document.getElementById('score').textContent = score;
        document.getElementById('total').textContent = totalQuestions;
        document.getElementById('quiz-result').style.display = 'block';

        // Evt. give points, hvis alt er korrekt
        if (score === totalQuestions) {
            fetch('/give-points', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    opgave_id: 10,
                    points: 1
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Du har fået points',
                        text: 'Dine points er blevet gemt', 
                        confirmButtonText: 'OK'
                    }).then(() => {
                        location.reload(); // Genindlæs siden for at opdatere points
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Du har allerede løst disse opgaver',
                        confirmButtonText: 'OK'
                    });
                }
            })
            .catch(error => {
                console.error('Error:', error);
                Swal.fire({
                    icon: 'error',
                    title: 'Fejl...',
                    text: 'Der opstod en fejl under kommunikationen med serveren.',
                    confirmButtonText: 'OK'
                });
            });
        }
    }

    // Nulstil alm. quiz
    function resetQuiz() {
        document.getElementById('quiz-form').reset();
        document.getElementById('quiz-result').style.display = 'none';
    }


    // ------ SVÆR OPGAVE QUIZ ------
    function checkAnswersHard() {
        console.log("checkAnswersHard() blev kaldt");
        let score = 0;
        const totalQuestions = 1;  // Kun 1 spørgsmål her

        // Tjek svær opgave
        const q1 = document.querySelector('input[name="hardQuestion1"]:checked');
        // Rigtigt svar var "3" (dvs. x = 1/2 og x = 2)
        if (q1 && q1.value === "3") {
            score++;
        }

        // Vis resultat for svær opgave
        document.getElementById('score-hard').textContent = score;
        document.getElementById('total-hard').textContent = totalQuestions;
        document.getElementById('quiz-result-hard').style.display = 'block';

        // Evt. give points, hvis alt er korrekt
        if (score === totalQuestions) {
            fetch('/give-points', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    opgave_id: 11,  // Evt. et andet opgave-id end 10
                    points: 5       // Evt. en anden pointsværdi
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Du har fået points (svær opgave)',
                        text: 'Dine points er blevet gemt', 
                        confirmButtonText: 'OK'
                    }).then(() => {
                        location.reload(); 
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Du har allerede løst disse opgaver',
                        confirmButtonText: 'OK'
                    });
                }
            })
            .catch(error => {
                console.error('Error:', error);
                Swal.fire({
                    icon: 'error',
                    title: 'Fejl...',
                    text: 'Der opstod en fejl under kommunikationen med serveren.',
                    confirmButtonText: 'OK'
                });
            });
        }
    }

    // Nulstil svær opgave quiz
    function resetQuizHard() {
        document.getElementById('quiz-form-hard').reset();
        document.getElementById('quiz-result-hard').style.display = 'none';
    }

