// Dynamic behaviour definitions for the general user interface
$(document).ready(function() {
  // Main menu needs to be hidden immediately as the page is loaded
  // The user will see it slide up on page load - this is intentional
  // so that they notice the availability of a drop down menu
  $('#home-toggle-dropdown').slideUp();

  $('#home-toggle-menu').click(function(){
    $('#home-toggle-dropdown').slideToggle();
  });

  $('.home-menu-link').click(function(){
    $('#home-toggle-dropdown').slideToggle();
  });

  $('.home-menu-item').mouseenter(function() {
    $(this).find('.home-menu-text').removeClass('home-menu-text-hide').addClass('home-menu-text-show');
  });

  $('.home-menu-item').mouseleave(function() {
    $(this).find('.home-menu-text').removeClass('home-menu-text-show').addClass('home-menu-text-hide');
  });

  $('.nav-menu').mouseleave(function() {
    $('#home-toggle-dropdown').slideUp();
  });

});
