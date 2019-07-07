$(function () {
    var dateFormat = "yy-mm-dd";
    var $from_date_input = $('input[name="from_date"]');
    var from_default_date = $from_date_input.val();
    from = $from_date_input
        .datepicker().datepicker("option", "dateFormat", dateFormat).datepicker("setDate", from_default_date).datepicker(
            "option", "showAnim", "fadeIn"
        )
        .on("change", function () {
            to.datepicker("option", "minDate", getDate(this));
        });
    var $to_date_input = $('input[name="to_date"]');
    var to_default_date = $to_date_input.val();
    to = $to_date_input
        .datepicker().datepicker("option", "dateFormat", dateFormat).datepicker("setDate", to_default_date).datepicker(
            "option", "showAnim", "fadeIn"
        ).on("change", function () {
            from.datepicker("option", "maxDate", getDate(this));
        });

    function getDate(element) {
        var date;
        try {
            date = $.datepicker.parseDate(dateFormat, element.value);
        } catch (error) {
            date = null;
        }

        return date;
    }
});
