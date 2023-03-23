document.addEventListener('DOMContentLoaded', function() {
    $('.selectpicker').selectpicker();
    document.querySelectorAll('.add-interval').forEach(btn =>{
        btn.addEventListener('click', (btn) => {
            AddTimePeriod(btn);
        });
    })
    document.querySelectorAll('.delete-interval').forEach(btn =>{
        btn.addEventListener('click', (btn) => {
            DeleteTimePeriod(btn);
        });
    })
    document.querySelectorAll('.field-type').forEach(field =>{
        field.addEventListener('change', (selectpicker) => {
            step = selectpicker.srcElement.parentElement.parentElement.parentElement;
            changeFieldType(step)
        })
    })
    document.querySelectorAll('.add-field-btn').forEach(btn =>{
        btn.addEventListener('click', (btn) => {
            AddField(btn);
            addFieldTypeListener(btn);
        });
    });
    document.querySelectorAll('.delete-field').forEach(btn =>{
        btn.addEventListener('click', (btn) => {deleteField(btn)});
    });
    document.querySelectorAll('.previous-field-btn').forEach(btn =>{
        btn.addEventListener('click', (btn) => {
            StepBack(btn);
            btn.srcElement.parentElement.parentElement.querySelector('.next-field-btn').disabled = false;
        });
    })
    document.querySelectorAll('.next-field-btn').forEach(btn =>{
        btn.addEventListener('click', (btn) => {
            StepForward(btn);
        });
    });
    document.querySelectorAll('.add-report-btn').forEach(btn => {
        btn.addEventListener('click', (btn) => {
            SaveReports(btn);
        })
    }) 
    document.querySelectorAll('.edit-report-btn').forEach(btn => {
        btn.addEventListener('click', (btn) => {
            SaveReports(btn);
        })
    })  
    $(".monthpicker").datepicker({
        format: "mm/yyyy",
        startView: "months",
        minViewMode: "months",
        language: 'ru-RU',
        endDate: "0m"
    });
    $(".yearpicker").datepicker({
        format: "yyyy",
        startView: "years",
        minViewMode: "years",
        language: 'ru-RU',
        startDate: "2020y",
        endDate: "+0y"
    });
    $.fn.datepicker.dates['qtrs'] = {
        days: ["Sunday", "Moonday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
        daysShort: ["Sun", "Moon", "Tue", "Wed", "Thu", "Fri", "Sat"],
        daysMin: ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"],
        months: ["Q1", "Q2", "Q3", "Q4", "", "", "", "", "", "", "", ""],
        monthsShort: ["Q1", "Q2", "Q3", "Q4", "", "", "", "", "", "", "", ""],
        today: "Today",
        clear: "Clear",
        format: "mm/dd/yyyy",
        titleFormat: "MM yyyy",
        /* Leverages same syntax as 'format' */
        weekStart: 0
      };
      
      $('.quarter').datepicker({
        format: "MM yyyy",
        minViewMode: 1,
        autoclose: true,
        language: "qtrs",
        forceParse: false
      }).on("show", function(event) {
      
        $(".month").each(function(index, element) {
          if (index > 3) $(element).hide();
        });
        
      });
})

function changeFieldType(step) {
    selectpicker = step.querySelector('.field-type select')
    step.querySelectorAll('.common-field').forEach(field =>{
        field.style.display = 'none'
    })
    step.querySelectorAll('.event-field').forEach(field =>{
        field.style.display = 'none'
    })
    step.querySelectorAll('.program-field').forEach(field =>{
        field.style.display = 'none'
    })
    step.querySelectorAll('.ppl-field').forEach(field =>{
        field.style.display = 'none'
    })
    if (selectpicker.value != "") {
        step.querySelectorAll('.common-field').forEach(field =>{
            field.style.display = 'block'
        })
        if (selectpicker.value == "VNTS" || selectpicker.value == "VNTSPPL") {
            step.querySelectorAll('.event-field').forEach(field =>{
                field.style.display = 'block'
            })
        }
        if (selectpicker.value == "PRGM" || selectpicker.value == "PRGMPPL") {
            step.querySelectorAll('.program-field').forEach(field =>{
                field.style.display = 'block'
            })
        }
        if (selectpicker.value == "PRGMPPL" || selectpicker.value == "VNTSPPL") {
            step.querySelectorAll('.ppl-field').forEach(field =>{
                field.style.display = 'block'
            })
        }
    }
}

function addFieldTypeListener(btn) {
    const modal = btn.srcElement.parentElement.parentElement;
    step = modal.querySelector('.current-step');
    step.querySelector('.field-type').addEventListener('change', (selectpicker) => {
            changeFieldType(step)
        })
    };

function deleteField(btn) {
    const modal = btn.srcElement.parentElement.parentElement.parentElement.parentElement
    modal.querySelector('.previous-field-btn').click();
    const field = btn.srcElement.parentElement;
    try {
        modal.querySelector(`[data-field="${parseInt(field.dataset.field) + 1}"]`).classList.add("next-step");
    } catch (error) {
        modal.querySelector('.add-field-btn').disabled = true;
        modal.querySelector('.next-field-btn').disabled = false;
        if (modal.parentElement.parentElement.classList.contains('edit-report-modal')) {
            modal.querySelector('.edit-report-btn').disabled = true;
        } else {
            modal.querySelector('.add-report-btn').disabled = true;
        }
    }
    field.remove();
    modal.querySelector('.fields_count').value = parseInt(modal.querySelector('.fields_count').value) - 1
    let field_number = 1;
    modal.querySelectorAll('.field-step').forEach(step =>{
        step.dataset.field = field_number;
        step.querySelector('.field-name').setAttribute("name", `field_name_${field_number}`);
        step.querySelector('.selectpicker.field-type').setAttribute("name", `field_type_${field_number}`);
        step.querySelector('.selectpicker.tags').setAttribute("name", `tags_${field_number}`);
        step.querySelector('.selectpicker.disabilities').setAttribute("name", `disabilities_${field_number}`);
        step.querySelector('.selectpicker.stop-tags').setAttribute("name", `stop_tags_${field_number}`);
        step.querySelector('.selectpicker.projects').setAttribute("name", `projects_${field_number}`);
        step.querySelector('.selectpicker.competencies').setAttribute("name", `competencies_${field_number}`);
        step.querySelector('.selectpicker.event-types').setAttribute("name", `event_types_${field_number}`);
        step.querySelector('.selectpicker.sex').setAttribute("name", `sex_${field_number}`);
        step.querySelector('.age_limit_max').setAttribute("name", `age_limit_max_${field_number}`);
        step.querySelector('.age_limit_min').setAttribute("name", `age_limit_min_${field_number}`);
        field_number += 1;
    })
    if (field_number === 2) {
        modal.querySelector('.delete-field').style.display = 'none';
    } else {
        modal.querySelectorAll('.delete-field').forEach(btn => {
            btn.style.display = 'block';
        })
    }
}

function checkStepValidity(current_step) {
    let step_is_valid = true
    current_step.querySelectorAll('input').forEach(input =>{
        if (!(input.reportValidity())){
            step_is_valid = false
        }
    })
    return step_is_valid
}

function StepForward(btn) {
    const modal = btn.srcElement.parentElement.parentElement;
    console.log(modal)
    const previous_step = modal.querySelector('.previous-step');
    const current_step = modal.querySelector('.current-step');
    const next_step = modal.querySelector('.next-step');
    if (checkStepValidity(current_step)) {
        if(!!previous_step){previous_step.classList.remove("previous-step");};
        current_step.classList.remove("current-step");
        current_step.classList.add("previous-step");
        next_step.classList.remove("next-step");
        next_step.classList.add("current-step");
        const steps_count = modal.querySelectorAll('.field-step').length;
        if (parseInt(next_step.dataset.field) < steps_count) {
            if (next_step.dataset.field == '1'){
                try {
                    modal.querySelector('[data-field="2"]').classList.add("next-step");
                }
                catch (error) {}
            } else {
                modal.querySelector(`[data-field="${parseInt(next_step.dataset.field) + 1}"]`).classList.add("next-step");
            }
        } else {
            modal.querySelector('.next-field-btn').disabled = true;
            modal.querySelector('.add-field-btn').disabled = false;
        }
        modal.querySelector('.previous-field-btn').disabled = false;
        if (modal.querySelectorAll(`.next-step`).length === 0) {
            if (modal.parentElement.parentElement.classList.contains('edit-report-modal')) {
                modal.querySelector('.edit-report-btn').disabled = false;
            } else {
                modal.querySelector('.add-report-btn').disabled = false;
            }
        };
        changeFieldType(next_step)
    }
}

function StepBack(btn) {
    const modal = btn.srcElement.parentElement.parentElement;
    const previous_step = modal.querySelector('.previous-step');
    const current_step = modal.querySelector('.current-step');
    const next_step = modal.querySelector('.next-step');

    previous_step.classList.remove("previous-step");
    previous_step.classList.add("current-step");

    if(!!next_step){next_step.classList.remove("next-step");};
    
    current_step.classList.remove("current-step");
    current_step.classList.add("next-step");

    if(previous_step.classList.contains('intervals-step')){
        modal.querySelector('.previous-field-btn').disabled = true;
    } else {
        if (previous_step.dataset.field == '2') {
            modal.querySelector('[data-field="1"]').classList.add("previous-step");
        } else if (previous_step.dataset.field == '1') {
            modal.querySelector('.intervals-step').classList.add("previous-step");
        } else {
            console.log(previous_step.previousElementSibling)
            previous_step.previousElementSibling.classList.add("previous-step");
        }
    }
    modal.querySelector('.add-field-btn').disabled = true;
    if (modal.parentElement.parentElement.classList.contains('edit-report-modal')) {
        modal.querySelector('.edit-report-btn').disabled = false;
    } else {
        modal.querySelector('.add-report-btn').disabled = false;
    }
}

function AddField(btn) {
    const modal = btn.srcElement.parentElement.parentElement;
    const previous_step = modal.querySelector('.previous-step');
    const current_step = modal.querySelector('.current-step');
    if (checkStepValidity(current_step)) {
        if(!!previous_step){
            previous_step.classList.remove("previous-step");
        }
        current_step.classList.remove("current-step");
        current_step.classList.add("previous-step");
        if (current_step.classList.contains('intervals-step')) {
            modal.querySelector('.field-step').classList.add("current-step");
            if(modal.querySelectorAll('.time-period').length === 1){
                modal.querySelectorAll('.dropdown-toggle').forEach(input =>{input.click();});
            }
        }else{
            const field_number = parseInt(current_step.dataset.field) + 1;
            const clone = document.querySelector('.field-step').cloneNode(true);
            clone.querySelector('.field-name').setAttribute("name", `field_name_${field_number}`);
            clone.querySelector('.field-name').value = "";
            clone.querySelector('.selectpicker.field-type').setAttribute("name", `field_type_${field_number}`);
            clone.querySelector('.selectpicker.tags').setAttribute("name", `tags_${field_number}`);
            clone.querySelector('.selectpicker.disabilities').setAttribute("name", `disabilities_${field_number}`);
            clone.querySelector('.selectpicker.stop-tags').setAttribute("name", `stop_tags_${field_number}`);
            clone.querySelector('.selectpicker.projects').setAttribute("name", `projects_${field_number}`);
            clone.querySelector('.selectpicker.competencies').setAttribute("name", `competencies_${field_number}`);
            clone.querySelector('.selectpicker.event-types').setAttribute("name", `event_types_${field_number}`);
            clone.querySelector('.selectpicker.sex').setAttribute("name", `sex_${field_number}`);
            clone.querySelector('.age_limit_max').setAttribute("name", `age_limit_max_${field_number}`);
            clone.querySelector('.age_limit_min').setAttribute("name", `age_limit_min_${field_number}`);
            clone.querySelectorAll('.common-field').forEach(field =>{field.style.display = 'none'})
            clone.querySelectorAll('.event-field').forEach(field =>{field.style.display = 'none'})
            clone.querySelectorAll('.program-field').forEach(field =>{field.style.display = 'none'})
            clone.querySelectorAll('.ppl-field').forEach(field =>{field.style.display = 'none'})
            modal.querySelector(`.add-report-form`).appendChild(clone);
            clone.dataset.field = field_number;
            clone.classList.remove("previous-step");
            clone.classList.add("current-step");
            $('.selectpicker').selectpicker('render');
            modal.querySelector('.current-step').querySelectorAll('.mb-3.select-field').forEach(input =>{
                    input.lastElementChild.lastElementChild.remove();
                    input.lastElementChild.lastElementChild.remove();
                })
        };
        modal.querySelector('.previous-field-btn').disabled = false;
        if (modal.querySelectorAll(`.next-step`).length === 0) {
            if (modal.parentElement.parentElement.classList.contains('edit-report-modal')) {
                modal.querySelector('.edit-report-btn').disabled = false;
            } else {
                modal.querySelector('.add-report-btn').disabled = false;
            }
        };
        modal.querySelector('.fields_count').value = parseInt(modal.querySelector('.fields_count').value) + 1
    }
}

function AddTimePeriod(btn) {
    const periods = btn.srcElement.parentElement;
    let interval_count = periods.querySelectorAll('.time-period').length;
    if(interval_count === 1){
        periods.querySelectorAll('.dropdown-toggle').forEach(input =>{input.click();});
    }
    const clone = periods.querySelector(`.time-period`).cloneNode(true);
    clone.querySelector('label').innerHTML = `Временной интервал №${interval_count + 1}`;
    clone.querySelector('.bootstrap-select.period-type').setAttribute("name", `period_type_${interval_count + 1}`);
    clone.querySelector('.selectpicker.period-type').setAttribute("name", `period_type_${interval_count + 1}`);
    clone.querySelector('.bootstrap-select.interval-type').setAttribute("name", `interval_type_${interval_count + 1}`);
    clone.querySelector('.selectpicker.interval-type').setAttribute("name", `interval_type_${interval_count + 1}`);
    clone.querySelector('.delete-interval').style.display = 'Block';
    clone.querySelector('.delete-interval').addEventListener('click', (btn) => {
        DeleteTimePeriod(btn);
    });
    periods.querySelector(`.time-periods`).appendChild(clone);
    periods.parentElement.querySelector('.periods_count').value = parseInt(periods.parentElement.querySelector('.periods_count').value) + 1
    $('.selectpicker.period-type').selectpicker('render');
    $('.selectpicker.interval-type').selectpicker('render');
    clone.querySelector('.bootstrap-select.period-type').lastElementChild.remove();
    clone.querySelector('.bootstrap-select.period-type').lastElementChild.remove();
    clone.querySelector('.bootstrap-select.interval-type').lastElementChild.remove();
    clone.querySelector('.bootstrap-select.interval-type').lastElementChild.remove();
}

function DeleteTimePeriod(btn) {
    const period = btn.srcElement.parentElement.parentElement.parentElement;
    const time_periods = period.parentElement.parentElement.parentElement;
    btn.srcElement.parentElement.parentElement.parentElement.remove();
    let period_number = 1
    time_periods.querySelector('.periods_count').value = parseInt(time_periods.querySelector('.periods_count').value) - 1
    time_periods.querySelectorAll('.time-period').forEach(timeperiod =>{
        timeperiod.querySelector('label').innerHTML = `Временной интервал №${period_number}`;
        timeperiod.querySelector('.bootstrap-select.period-type').setAttribute("name", `period_type_${period_number}`);
        timeperiod.querySelector('.selectpicker.period-type').setAttribute("name", `period_type_${period_number}`);
        timeperiod.querySelector('.bootstrap-select.interval-type').setAttribute("name", `interval_type_${period_number}`);
        timeperiod.querySelector('.selectpicker.interval-type').setAttribute("name", `interval_type_${period_number}`);
        period_number += 1
    })
}

function SaveReports(btn){
    document.querySelectorAll('.dropdown-toggle').forEach(input => {input.click()});
    const modal = btn.srcElement.parentElement.parentElement.parentElement.parentElement

    const report = { 
        name: modal.querySelector('.report-name').value,
        fields_count: modal.querySelector('.fields_count').value,
        periods_count: modal.querySelector('.periods_count').value,
    }
    if (modal.classList.contains('add-report-modal')) {
        console.log(true)
        report['is_new'] = true;
    } else {
        console.log(false)
        report['is_new'] = false;
        report['id'] = modal.querySelector('.report-id').value;
    }

    modal.querySelectorAll('.selectpicker.period-type').forEach(input =>{report[input.name] = input.value;})
    modal.querySelectorAll('.selectpicker.interval-type').forEach(input =>{report[input.name] = input.value;})
    modal.querySelectorAll('.field-name').forEach(input =>{report[input.name] = input.value;})
    modal.querySelectorAll('.field-type').forEach(input =>{report[input.name] = input.value;})
    modal.querySelectorAll('.age_limit_max').forEach(input =>{report[input.name] = input.value;})
    modal.querySelectorAll('.age_limit_min').forEach(input =>{report[input.name] = input.value;})
    modal.querySelectorAll('.selectpicker.tags').forEach(input =>{
        console.log("tags")
        console.log(input.parentElement)
        console.log(input.parentElement.querySelectorAll('li.selected'))
        const selected_li = Array.from(input.parentElement.querySelectorAll('li.selected'))
        console.log(selected_li)
        report[input.name] = selected_li.map(li => li.querySelector('.text').innerHTML);
    })
    modal.querySelectorAll('.selectpicker.field-input').forEach(input =>{
        const selected_li = Array.from(input.parentElement.querySelectorAll('li.selected'))
        report[input.name] = selected_li.map(li => li.querySelector('.text').innerHTML);
    })
    
    console.log(report)

   fetch('/reports/', {
            method: 'POST',
            body: JSON.stringify(report)
        })
        .then(response => response.json())
        .then(result => {
            if(result['message'] === 'OK'){
                location.reload()
                console.log(result)
            }
        })
}