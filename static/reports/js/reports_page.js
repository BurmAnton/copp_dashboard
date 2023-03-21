document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.add-interval').addEventListener('click', (btn) => {
        AddTimePeriod();
        document.querySelectorAll('.delete-interval').forEach(btn =>{
            btn.addEventListener('click', (btn) => {
                DeleteTimePeriod(btn);
            });
        })
    });
    document.querySelector('.add-field-btn').addEventListener('click', (btn) => {
        AddField();
        addFieldTypeListener();
    });
    document.querySelector('.previous-field-btn').addEventListener('click', (btn) => {
        StepBack();
        document.querySelector('.next-field-btn').style.display = 'block';
    });
    document.querySelector('.next-field-btn').addEventListener('click', (btn) => {
        StepForward();
    });
    document.querySelector('.add-report-btn').addEventListener('click', (btn) => {
        SaveReports();
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

function addFieldTypeListener() {
    step = document.querySelector('.current-step');
    step.querySelector('.field-type').addEventListener('change', (selectpicker) => {
            selectpicker = selectpicker.srcElement
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
            console.log(selectpicker.value)
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
        })
    };

function checkStepValidity(current_step) {
    let step_is_valid = true
    current_step.querySelectorAll('input').forEach(input =>{
        if (!(input.reportValidity())){
            step_is_valid = false
        }
    })
    return step_is_valid
}

function StepForward() {
    const previous_step = document.querySelector('.previous-step');
    const current_step = document.querySelector('.current-step');
    const next_step = document.querySelector('.next-step');
    if (checkStepValidity(current_step)) {
        if(!!previous_step){previous_step.classList.remove("previous-step");};
    
        current_step.classList.remove("current-step");
        current_step.classList.add("previous-step");

        next_step.classList.remove("next-step");
        next_step.classList.add("current-step");
    
        const steps_count = document.querySelectorAll('.field-step').length
        if (parseInt(next_step.dataset.field) < steps_count) {
            if (next_step.dataset.field == '1'){
                try {
                    document.querySelector('[data-field="2"]').classList.add("next-step");
                }
                catch (error) {}
            } else {
                next_step.nextSibling.classList.add("next-step");
            }
        } else {
            document.querySelector('.next-field-btn').style.display = 'none';
            document.querySelector('.add-field-btn').style.display = 'block';
        }
        document.querySelector('.previous-field-btn').style.display = 'block';
        if (document.querySelectorAll(`.next-step`).length === 0) {
            document.querySelector('.add-report-btn').style.display = 'block';
        };  
    }
}

function StepBack() {
    const previous_step = document.querySelector('.previous-step');
    const current_step = document.querySelector('.current-step');
    const next_step = document.querySelector('.next-step');

    previous_step.classList.remove("previous-step");
    previous_step.classList.add("current-step");

    if(!!next_step){next_step.classList.remove("next-step");};
    
    current_step.classList.remove("current-step");
    current_step.classList.add("next-step");

    if(previous_step.classList.contains('intervals-step')){
        document.querySelector('.previous-field-btn').style.display = 'none';
    } else {
        if (previous_step.dataset.field == '2') {
            document.querySelector('[data-field="1"]').classList.add("previous-step");
        } else if (previous_step.dataset.field == '1') {
            document.querySelector('.intervals-step').classList.add("previous-step");
        } else {
            previous_step.previousSibling.classList.add("previous-step");
        }
    }
    document.querySelector('.add-field-btn').style.display = 'none';
    document.querySelector('.add-report-btn').style.display = 'none';
}

function AddField() {
    const previous_step = document.querySelector('.previous-step');
    if(!!previous_step){
        previous_step.classList.remove("previous-step");
    }
    const current_step = document.querySelector('.current-step');
    if (checkStepValidity(current_step)) {
        current_step.classList.remove("current-step");
        current_step.classList.add("previous-step");
        if (current_step.classList.contains('intervals-step')) {
            document.querySelector('.field-step').classList.add("current-step");
            if(document.querySelectorAll('.time-period').length === 1){
                document.querySelectorAll('.dropdown-toggle').forEach(input =>{input.click();});
            }
        }else{
            const field_number = parseInt(current_step.dataset.field) + 1;
            const clone = document.querySelector('.field-step').cloneNode(true);
            clone.querySelector('.field-name').setAttribute("name", `field_name_${field_number}`);
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
            document.querySelector(`.add-report-form`).appendChild(clone);
            clone.dataset.field = field_number;
            clone.classList.remove("previous-step");
            clone.classList.add("current-step");
            $('.selectpicker').selectpicker('render');
                document.querySelector('.current-step').querySelectorAll('.mb-3.select-field').forEach(input =>{
                    input.lastElementChild.lastElementChild.remove();
                    input.lastElementChild.lastElementChild.remove();
                })
        };
        document.querySelector('.previous-field-btn').style.display = 'block';
        if (document.querySelectorAll(`.next-step`).length === 0) {
            document.querySelector('.add-report-btn').style.display = 'block';
        };
        document.querySelector('.fields_count').value = parseInt(document.querySelector('.fields_count').value) + 1
    }
}

function AddTimePeriod() {
    let interval_count = document.querySelectorAll('.time-period').length;
    if(interval_count === 1){
        document.querySelectorAll('.dropdown-toggle').forEach(input =>{input.click();});
    }
    const clone = document.querySelector(`.time-period`).cloneNode(true);
    clone.querySelector('label').innerHTML = `Временной интервал №${interval_count + 1}`;
    clone.querySelector('.bootstrap-select.period-type').setAttribute("name", `period_type_${interval_count + 1}`);
    clone.querySelector('.selectpicker.period-type').setAttribute("name", `period_type_${interval_count + 1}`);
    clone.querySelector('.bootstrap-select.interval-type').setAttribute("name", `interval_type_${interval_count + 1}`);
    clone.querySelector('.selectpicker.interval-type').setAttribute("name", `interval_type_${interval_count + 1}`);
    clone.querySelector('.delete-interval').style.display = 'Block';
    document.querySelector(`.time-periods`).appendChild(clone);
    document.querySelector('.periods_count').value = parseInt(document.querySelector('.periods_count').value) + 1
    $('.selectpicker.period-type').selectpicker('render');
    $('.selectpicker.interval-type').selectpicker('render');
    clone.querySelector('.bootstrap-select.period-type').lastElementChild.remove();
    clone.querySelector('.bootstrap-select.period-type').lastElementChild.remove();
    clone.querySelector('.bootstrap-select.interval-type').lastElementChild.remove();
    clone.querySelector('.bootstrap-select.interval-type').lastElementChild.remove();
}

function DeleteTimePeriod(btn) {
    btn.srcElement.parentElement.parentElement.parentElement.remove();
}

function SaveReports(){
    const report = { 
        name: document.querySelector('.report-name').value,
        fields_count: document.querySelector('.fields_count').value,
        periods_count: document.querySelector('.periods_count').value,
    }
    document.querySelectorAll('.selectpicker.period-type').forEach(input =>{report[input.name] = input.value;})
    document.querySelectorAll('.selectpicker.interval-type').forEach(input =>{report[input.name] = input.value;})
    document.querySelectorAll('.field-name').forEach(input =>{report[input.name] = input.value;})
    document.querySelectorAll('.field-type').forEach(input =>{report[input.name] = input.value;})
    document.querySelectorAll('.selectpicker.tags').forEach(input =>{
        const selected_li = Array.from(input.parentElement.querySelectorAll('li.selected'))
        report[input.name] = selected_li.map(li => li.querySelector('.text').innerHTML);
    })
    document.querySelectorAll('.selectpicker.field-input').forEach(input =>{
        const selected_li = Array.from(input.parentElement.querySelectorAll('li.selected'))
        report[input.name] = selected_li.map(li => li.querySelector('.text').innerHTML);
    })
    
    console.log(report)

    fetch('/reports/', {
            method: 'POST',
            body: JSON.stringify(report)
        })
        .then(response => response.json())
        .then(result => {})
}