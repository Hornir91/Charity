document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];

      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep++;
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          this.updateForm();
        });
      });

      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      // TODO: Validation

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

    }

    /**
     * Submit form
     *
     * TODO: validation, send data to server
     */
    submit(e) {

      this.currentStep++;
      this.updateForm();
    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }

  /**
   * AJAX call to get chosen institutions from step 1
   */
  $('#first-button').on('click', function () {
    let categories = $('.first-step');
    let categoriesChecked = [];

    for (let i=0; i<categories.length; i++) {
      if (categories[i].checked == true) {

        categoriesChecked.push(categories[i].value);
      }
    }
    $.ajax({
      url: '/third_step_filter/',
      type: "GET",
      traditional: true,
      data: {
        'categoriesChecked': categoriesChecked},
      }).done(function (data) {
        let parsedData = JSON.parse(data);
        let h3El = $('#third-h3');
        $.each(parsedData, function () {
          let newDiv = $('<div class="form-group form-group--checkbox"><label><input type="radio" name="organization" ' +
              'value="old" /><span class="checkbox radio"></span><span class="description"><div class="title">a</div><div class="subtitle">a\n' +
              '</div></span></label></div>');
          $(newDiv).find("div.title").text(this.fields.name);
          $(newDiv).find("div.subtitle").text(this.fields.description);
          $(newDiv).find("input[name='organization']").attr({
            'value': this.pk,
            'data-name': this.fields.name
          });
          h3El.after(newDiv);
        })
      }).fail(function () {
        alert("Coś poszło nie tak :(");
    }).always(function () {
      console.log("Połączenie wykonane poprawnie.")
    });
  });

  /**
   * Fills last-step form inputs with data from previous steps
   */
  $("#fourth-button").on('click', function () {
    let bags = $('input[name="bags"]').val();
    let institution = $('input[name="organization"]:checked').attr('data-name');
    let address = $('input[name="address"]').val();
    let city = $('input[name="city"]').val();
    let postcode = $('input[name="postcode"]').val();
    let phoneNumber = $('input[name="phone"]').val();
    let shipmentDate = $('input[name="data"]').val();
    let shipmentTime = $('input[name="time"]').val();
    let moreInfo = $('textarea[name="more_info"]').val();
    $('span#bags').html(bags + " worki rzeczy dla potrzebujących");
    $('span#institution').html("Dla " + institution);
    $('#first-column li:first-child').html(address);
    $('#first-column li:nth-child(2)').html(city);
    $('#first-column li:nth-child(3)').html(postcode);
    $('#first-column li:nth-child(4)').html(phoneNumber);
    $('#second-column li:first-child').html(shipmentDate);
    $('#second-column li:nth-child(2)').html(shipmentTime);
    $('#second-column li:nth-child(3)').html(moreInfo);
  });

  /**
   * User-profile donation list event
   * This AJAX make GET call to change "is_taken" value to True and moves whole <li> to <ul id="taken">
   * (completed donations)
   */
  let lastChildDonationCheck = $('.donation').find('input:checkbox');
  lastChildDonationCheck.each(function (index) {
    $(this).change(function () {
      $.ajax({
      url: '/is_taken_change/',
      type: 'GET',
      traditional: true,
      data: {
        "checked_status": this.checked,
        "donation_id": this.dataset.donationid
      }}).done(function (data) {
        let donationComplete = JSON.parse(data);
        let parent = $("div [data-divdonationid=" + donationComplete[0].pk + "]");
        parent.toggleClass("donation_complete");
        parent.find('label').hide();
        parent.appendTo($('#taken'));
      }).fail(function (data) {
        alert(data);
      }).always(console.log("Connection completed"))
    })
  });

  /**
   * Password requirement for edit user informations
   */
  $('#user_edit').on('click', function (event) {
    event.preventDefault();
    $('.pop-up').css('display', 'block');
    $('.pop-up-container').css('display', 'block');
  });
});
