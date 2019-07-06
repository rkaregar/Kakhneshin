$(function () {
    var dateFormat = "yy-mm-dd";
    from = $('input[name="from_date"]')
        .datepicker().datepicker(
            "option", "showAnim", "fadeIn"
        ).datepicker("option", "dateFormat", dateFormat)
        .on("change", function () {
            to.datepicker("option", "minDate", getDate(this));
        });
    to = $('input[name="to_date"]')
        .datepicker().datepicker(
            "option", "showAnim", "fadeIn"
        ).datepicker("option", "dateFormat", dateFormat)
        .on("change", function () {
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
