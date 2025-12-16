document.addEventListener('DOMContentLoaded', function() {


    const ageInput = document.getElementById("age");
    const weightInput = document.getElementById("weight");
    const heightInput = document.getElementById("height");
    const sexValue = document.getElementById('sex_value'); 
    const workoutAmount = document.getElementById('workout_amount'); 
    const workoutGroup = document.getElementById('workout_group');
    const sexGroup = document.getElementById('sex_group');
    const goalGroup = document.getElementById('goal_group');
    const goalValue = document.getElementById('goal_value');
    const nextButton1 = document.getElementById('next_page1');
    const nextButton2 =  document.getElementById('next_page2');
    const nextButton3 =  document.getElementById('next_page3');
    const weightGoal = document.getElementById('weight_goal');
    const prevButton1 = document.getElementById('prev_page1');
    const prevButton2 = document.getElementById('prev_page2');
    const speedValue = document.getElementById('speed_value');
    const speedQuestion = document.getElementById('speed_question');
    const planValue = document.getElementById('plan_value'); 
    const planGroup = document.getElementById('plan_group');
    const initText = document.getElementById('init_text');
    const infoText = document.getElementById('info_txt');
    const loadImage = document.getElementById('load_img');
    const loadTextDuration = 1500;
    const loadText1 = document.getElementById('load_txt1');
    const loadText2 = document.getElementById('load_txt2');
    const loadText3 = document.getElementById('load_txt3');
    const loadText4 = document.getElementById('load_txt4');
    const loadText5 = document.getElementById('load_txt5');
    let showOutputs = false;
    const welcomeBox = document.getElementById('welcome_box');
    const generatePlanName = 'generatePlan';
    const generatePlanEvent = new CustomEvent(generatePlanName);
    const topMenuDiv = document.getElementById('top_menu');
    const body = document.getElementById('body');
    const break1 = document.getElementById('break1');
    const break2 = document.getElementById('break2');
    const break3 = document.getElementById('break3');
    const break4 = document.getElementById('break4');
    const break5 = document.getElementById('break5');
    const break6 = document.getElementById('break6');
    const break7 = document.getElementById('break7');
    const break8 = document.getElementById('break8');
    const startupButton = document.getElementById('create_plan');
    const repnImg = document.getElementById('repn_img');
    const repnTxt = document.getElementById('repn_init_text');
    

    const bedTimeInput = document.getElementById('bed_time'); 
    const weightGoalInput = document.getElementById('weight_goal');
    

    const recalculateBtn = document.getElementById('recalculate-btn');

    startupButton.addEventListener('click', function() {
        startupButton.classList.add('is-hidden');
        repnImg.classList.add('is-hidden');
        repnTxt.classList.add('is-hidden');
        ageInput.classList.remove('is-hidden');
        weightInput.classList.remove('is-hidden');
        heightInput.classList.remove('is-hidden');
        sexGroup.classList.remove('is-hidden');
        nextButton1.classList.remove('is-hidden');
        initText.classList.remove('is-hidden');
        infoText.classList.remove('is-hidden');

    });


    nextButton1.addEventListener('click', function() {
        workoutGroup.classList.remove('is-hidden');
        ageInput.classList.add('is-hidden');
        weightInput.classList.add('is-hidden');
        heightInput.classList.add('is-hidden');
        sexGroup.classList.add('is-hidden');
        goalGroup.classList.remove('is-hidden');
        nextButton1.classList.add('is-hidden');
        nextButton2.classList.remove('is-hidden');
        weightGoal.classList.remove('is-hidden');
        prevButton1.classList.remove('is-hidden');
        break1.classList.add('is-hidden');
        break2.classList.add('is-hidden');
        break3.classList.add('is-hidden');
        break4.classList.add('is-hidden');
        break5.classList.add('is-hidden');
        break6.classList.add('is-hidden');
        break8.classList.add('is-hidden');
        
        

    });

    prevButton1.addEventListener('click', function() {
        workoutGroup.classList.add('is-hidden');
        ageInput.classList.remove('is-hidden');
        weightInput.classList.remove('is-hidden');
        heightInput.classList.remove('is-hidden');
        sexGroup.classList.remove('is-hidden');
        goalGroup.classList.add('is-hidden');
        nextButton1.classList.remove('is-hidden');
        nextButton2.classList.add('is-hidden');
        weightGoal.classList.add('is-hidden');
        prevButton1.classList.add('is-hidden');
        

        
        break1.classList.remove('is-hidden');
        break2.classList.remove('is-hidden');
        break3.classList.remove('is-hidden');
        break4.classList.remove('is-hidden');
        break5.classList.remove('is-hidden');
        break6.classList.remove('is-hidden');
        break8.classList.remove('is-hidden');
    });
    
    nextButton2.addEventListener('click', function() {
        workoutGroup.classList.add('is-hidden');
        goalGroup.classList.add('is-hidden');
        nextButton2.classList.add('is-hidden');
        weightGoal.classList.add('is-hidden');
        prevButton1.classList.add('is-hidden');
        prevButton2.classList.remove('is-hidden');
        nextButton3.classList.remove('is-hidden');
        break7.classList.add('is-hidden');
        

        document.getElementById('sleep_group').classList.remove('is-hidden'); 

        if (goalValue.value=='bulk') {
            speedQuestion.classList.remove('is-hidden');
            speedQuestion.textContent = 'How quickly do you want to gain weight?';
            speedValue.classList.remove('is-hidden');
            planGroup.classList.remove('is-hidden');
        }
        else if (goalValue.value=='cut') {
            speedQuestion.classList.remove('is-hidden');
            speedQuestion.textContent = 'How quickly do you want to loose weight?';
            speedValue.classList.remove('is-hidden');
            planGroup.classList.remove('is-hidden');
        }
        else if (goalValue.value=='maintain') {
            planGroup.classList.remove('is-hidden');
        }
    });   
        
    prevButton2.addEventListener('click', function() {
        workoutGroup.classList.remove('is-hidden');
        goalGroup.classList.remove('is-hidden');
        nextButton2.classList.remove('is-hidden');
        weightGoal.classList.remove('is-hidden');
        prevButton1.classList.remove('is-hidden');
        prevButton2.classList.add('is-hidden');
        nextButton3.classList.add('is-hidden');
        speedQuestion.classList.add('is-hidden');
        speedValue.classList.add('is-hidden');
        planGroup.classList.add('is-hidden');
        break7.classList.remove('is-hidden');
        

        document.getElementById('sleep_group').classList.add('is-hidden'); 
    });

    
    nextButton3.addEventListener('click', function() {
        prevButton2.classList.add('is-hidden');
        nextButton3.classList.add('is-hidden');
        speedQuestion.classList.add('is-hidden');
        speedValue.classList.add('is-hidden');
        planGroup.classList.add('is-hidden');
        initText.classList.add('is-hidden');
        infoText.classList.add('is-hidden');
        loadImage.classList.remove('is-hidden');
        
        
        document.getElementById('sleep_group').classList.add('is-hidden'); 
        welcomeBox.style = "background-color: black;";


        loadText1.classList.remove('is-hidden');
        setTimeout(function() {
            loadText1.classList.add('is-hidden');
            loadText2.classList.remove('is-hidden');
            setTimeout(function() {
                loadText2.classList.add('is-hidden');
                loadText3.classList.remove('is-hidden');
                setTimeout(function() {
                    loadText3.classList.add('is-hidden');
                    loadText4.classList.remove('is-hidden');
                    setTimeout(function() {
                        loadText4.classList.add('is-hidden');
                        loadText5.classList.remove('is-hidden');
                        setTimeout(function() {
                            loadText5.classList.add('is-hidden');
                            loadImage.classList.add('is-hidden');
                            document.dispatchEvent(generatePlanEvent);
                        }, loadTextDuration);
                    }, loadTextDuration);
                }, loadTextDuration);
            }, loadTextDuration);
        }, loadTextDuration);
    });

    
    function resetForm() {
        
        ageInput.classList.remove('is-hidden');
        weightInput.classList.remove('is-hidden');
        heightInput.classList.remove('is-hidden');
        sexGroup.classList.remove('is-hidden');
        
        
        document.getElementById('sleep_group').classList.add('is-hidden');
        nextButton1.classList.remove('is-hidden');

        
        workoutGroup.classList.add('is-hidden');
        goalGroup.classList.add('is-hidden');
        nextButton2.classList.add('is-hidden');
        weightGoal.classList.add('is-hidden');
        prevButton1.classList.add('is-hidden');
        prevButton2.classList.add('is-hidden');
        nextButton3.classList.add('is-hidden');
        speedQuestion.classList.add('is-hidden');
        speedValue.classList.add('is-hidden');
        planGroup.classList.add('is-hidden');
        initText.classList.remove('is-hidden');
        infoText.classList.remove('is-hidden');

        
        welcomeBox.style = "background-color: #333;";

        
        break1.classList.remove('is-hidden');
        break2.classList.remove('is-hidden');
        break3.classList.remove('is-hidden');
        break4.classList.remove('is-hidden');
        break5.classList.remove('is-hidden');
        break6.classList.remove('is-hidden');
        break7.classList.remove('is-hidden');
        break8.classList.remove('is-hidden');
    }

    
    recalculateBtn.addEventListener('click', function(e) {
        e.preventDefault(); 
        
        
        document.getElementById('dashboard_container').classList.add('is-hidden');

        
        welcomeBox.classList.remove('is-hidden');
        
        
        body.style = "background-color: #00031c;";

        
        resetForm();
    });


    
    async function callBackendAPI() {
        console.log("Gathering data and calling backend...");

        
        const activityMap = {
            'lightly_active': 'lightly active',
            'active': 'active', 
            'very_active': 'very active',
            'extra_active': 'extra active'
        };
        const planMap = {
            'strength': 'strength',
            'muscle': 'muscle',
            'both': 'hybrid'
        };

        const age = parseInt(ageInput.value, 10);
        const weight = parseFloat(weightInput.value);
        const height = parseFloat(heightInput.value);
        const gender = sexValue.value;
        const activity = activityMap[workoutAmount.value];
        const goal = goalValue.value;
        const loss_speed = speedValue.value || 'medium';
        const plan = planMap[planValue.value];
        const final_weight = parseFloat(weightGoalInput.value) || weight; 
        
        
        const bed_time = bedTimeInput.value; 

        const nutritionData = { age, gender, weight, height, activity, goal, loss_speed };
        const workoutData = { weight, plan, activity };
        const goalDateData = { current_weight: weight, final_weight: final_weight, loss_speed: loss_speed };
        const sleepData = { bed_time: bed_time };

        try {
            const [
                nutritionResponse,
                workoutResponse,
                goalDateResponse,
                sleepResponse
            ] = await Promise.all([
                fetch('http://127.0.0.1:5000/api/nutrition-plan', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(nutritionData)
                }),
                fetch('http://127.0.0.1:5000/api/workout-plan', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(workoutData)
                }),
                fetch('http://127.0.0.1:5000/api/date-to-goal', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(goalDateData)
                }),
                fetch('http://127.0.0.1:5000/api/sleep-calculator', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(sleepData)
                })
            ]);

            const nutritionResult = await nutritionResponse.json();
            const workoutResult = await workoutResponse.json();
            const goalDateResult = await goalDateResponse.json();
            const sleepResult = await sleepResponse.json();

            if (!nutritionResponse.ok) throw new Error(nutritionResult.error);
            if (!workoutResponse.ok) throw new Error(workoutResult.error);
            if (!goalDateResponse.ok) throw new Error(goalDateResult.error);
            if (!sleepResponse.ok) throw new Error(sleepResult.error);

            return {
                nutrition: nutritionResult,
                workout: workoutResult,
                goalDate: goalDateResult,
                sleep: sleepResult
            };

        } catch (error) {
            console.error("Failed to fetch plans:", error);
            alert(`Error generating plan: ${error.message}. Please check your inputs and try again.`);
            return null; 
        }
    }


    document.addEventListener('generatePlan', async function() {
        
        const planData = await callBackendAPI();

        if (planData) {
            console.log("Successfully fetched data:", planData);

            welcomeBox.classList.add('is-hidden');
            document.getElementById('dashboard_container').classList.remove('is-hidden');
            body.style = "background-color: #0B0F19;"; 
            
            
            const nutrition = planData.nutrition;
            const macros = nutrition.macronutrients;
            const otherInfo = nutrition.other_info;
            const targetDate = planData.goalDate.target_date;

            const calories = Math.round(nutrition.goal_calories);
            document.getElementById('calorie-goal').textContent = calories;

            const macroContainer = document.getElementById('macro-details');
            macroContainer.innerHTML = `
                <p style="font-size: 1.1rem; margin-top: 20px;"><strong>Protein:</strong> ${macros.protein_g}g</p>
                <p style="font-size: 1.1rem;"><strong>Carbs:</strong> ${macros.carbs_g}g</p>
                <p style="font-size: 1.1rem;"><strong>Fat:</strong> ${macros.fat_g}g</p>
            `;
            
            const otherContainer = document.getElementById('other-nutrition-details');
            otherContainer.innerHTML = `
                <p style="color: #aaa;">Fiber: ${otherInfo.fiber_g}g</p>
                <p style="color: #aaa;">Sugar Limit: ${otherInfo.sugar_g_limit}g</p>
                <p style="color: #aaa;">Sodium Limit: ${otherInfo.sodium_mg_limit}mg</p>
                <p style="color: #aaa;">Water: ${otherInfo.water_liters}L</p>
                <p style="color: #00A9FF; margin-top: 10px;">Target Date: <strong>${targetDate}</strong></p>
            `;
            
            
            const wakeTime = planData.sleep.wake_up_time;
            document.getElementById('wake-up-time').textContent = wakeTime;


            
            const workout1 = planData.workout.option_1;
            const workoutName1 = workout1.name || "PUSH-PULL-LEGS";
            document.getElementById('workout-split-name-1').textContent = workoutName1;
            
            const mainSplit1 = workoutName1.split(' ')[0];
            const splitDays1 = mainSplit1.split('-'); 

            const tagsContainer1 = document.getElementById('weekly-plan-tags-1');
            tagsContainer1.innerHTML = ''; 

            splitDays1.forEach(day => {
                const tag = document.createElement('span');
                tag.className = 'workout-tag';
                tag.textContent = day.toUpperCase();
                if (day.toUpperCase() === 'PUSH') tag.classList.add('push');
                else if (day.toUpperCase() === 'PULL') tag.classList.add('pull');
                else if (day.toUpperCase() === 'LEGS') tag.classList.add('legs');
                else tag.classList.add('pull');
                tagsContainer1.appendChild(tag);
            });

            
            const schedule1 = workout1.schedule; 
            const workoutContainer1 = document.getElementById('workout-plan-container-1');
            workoutContainer1.innerHTML = ''; 

            schedule1.forEach((day, index) => {
                const dayEl = document.createElement('div');
                dayEl.className = 'workout-day'; 
                let dayHtml = `<h3>Day ${index + 1}</h3><ul>`;
                
                day.forEach(exercise => {
                    dayHtml += `
                        <li>
                            <strong>${exercise.name}</strong>
                            <span>
                                ${exercise.sets} sets x ${exercise.reps} reps
                                <br>
                                ${exercise.rest_time} rest | Weight: ${exercise.weight} kg
                            </span>
                        </li>
                    `;
                });
                dayHtml += '</ul>';
                dayEl.innerHTML = dayHtml;
                workoutContainer1.appendChild(dayEl);
            });

            
            const workout2 = planData.workout.option_2;
            const dashGrid = document.querySelector('.dash-grid');
            const workoutCard2 = document.getElementById('workout-card-2');

            if (workout2.name === "") {
            
                workoutCard2.classList.add('is-hidden');
                dashGrid.style.gridTemplateColumns = '2fr 3fr';
            } else {
                workoutCard2.classList.remove('is-hidden');
                dashGrid.style.gridTemplateColumns = '2fr 3fr 3fr';

                const workoutName2 = workout2.name;
                document.getElementById('workout-split-name-2').textContent = workoutName2;
                
                const mainSplit2 = workoutName2.split(' ')[0];
                const splitDays2 = mainSplit2.split('-'); 

                const tagsContainer2 = document.getElementById('weekly-plan-tags-2');
                tagsContainer2.innerHTML = ''; 

                splitDays2.forEach(day => {
                    const tag = document.createElement('span');
                    tag.className = 'workout-tag';
                    tag.textContent = day.toUpperCase();
                    if (day.toUpperCase() === 'PUSH') tag.classList.add('push');
                    else if (day.toUpperCase() === 'PULL') tag.classList.add('pull');
                    else if (day.toUpperCase() === 'LEGS') tag.classList.add('legs');
                    else tag.classList.add('pull');
                    tagsContainer2.appendChild(tag);
                });

                const schedule2 = workout2.schedule; 
                const workoutContainer2 = document.getElementById('workout-plan-container-2');
                workoutContainer2.innerHTML = ''; 

                schedule2.forEach((day, index) => {
                    const dayEl = document.createElement('div');
                    dayEl.className = 'workout-day'; 
                    let dayHtml = `<h3>Day ${index + 1}</h3><ul>`;
                    
                    day.forEach(exercise => {
                        dayHtml += `
                            <li>
                                <strong>${exercise.name}</strong>
                                <span>
                                    ${exercise.sets} sets x ${exercise.reps} reps
                                    <br>
                                    ${exercise.rest_time} rest | Weight: ${exercise.weight} kg
                                </span>
                            </li>
                        `;
                    });
                    dayHtml += '</ul>';
                    dayEl.innerHTML = dayHtml;
                    workoutContainer2.appendChild(dayEl);
                });
            }

        } else {
            console.log("API call failed. Resetting to form.");
            alert('There was an error generating your plan. Please try again.');
            resetForm(); 
        }
    });
});
