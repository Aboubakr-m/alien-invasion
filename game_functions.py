import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets): 
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        # Move the ship to the right.
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # Move the ship to the right.
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        # Move the ship to the right.
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        # Move the ship to the right.
        ship.moving_down = True
    elif event.key == pygame.K_RETURN and not stats.game_active:
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)
    elif event.key == pygame.K_SPACE and stats.game_active:
        fire_bullet(ai_settings, screen, ship, bullets)
        ai_settings.bullet_sound.play()
    elif event.key == pygame.K_q:
        save_high_score(stats)
        sys.exit()

def check_keyup_events(event, ship):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        # Move the ship to the right.
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        # Move the ship to the right.
        ship.moving_down = False
        
def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_high_score(stats)
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
                
def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y) 
    if button_clicked and not stats.game_active:
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)
        
def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Start a new game when the player clicks Enter or Play."""
    play_music()
    # Reset the game settings.
    ai_settings.initialize_dynamic_settings()
    # Hide the mouse cursor.
    pygame.mouse.set_visible(False)
    # Reset the game statistics.
    stats.reset_stats()
    stats.game_active = True
    
    # Reset the scoreboard images.
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()
    
    # Empty the list of aliens and bullets.
    aliens.empty()
    bullets.empty()
    
    # Create a new fleet and center the ship.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()
        
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Update images on the screen and flip to the new screen."""
    # blit the screen with the background image
    img = pygame.transform.scale(ai_settings.bg, (1200, 800))
    screen.blit(img, (0, 0))
    
    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    
    # Draw the score information.
    sb.show_score()
    
    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()
        
    # update the display
    pygame.display.flip()
    
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Update position of bullets and get rid of old bullets."""
    bullets.update()
    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
         if bullet.rect.bottom <= 0:
             bullets.remove(bullet)
             
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)
        
    
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    
    if collisions:
        for aliens in collisions.values():    
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        ai_settings.incrase_speed()
        
        # Increase level.
        stats.level += 1
        sb.prep_level()
        
        create_fleet(ai_settings, screen, ship, aliens)
    
def fire_bullet(ai_settings, screen, ship, bullets):
    """Create a new bullet and add it to the bullets group."""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        
def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    avilable_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(avilable_space_x / (2 * alien_width))
    return number_aliens_x
    
def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    avilable_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(avilable_space_y / (3 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.y + 2 * alien.rect.height * row_number
    aliens.add(alien)
    
def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien and find the number of aliens in a row.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    
    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
            
def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
        
def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
        
def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        # play crash sound effect
        ai_settings.ship_crash_sound.play()
        # Decrement ships_left.
        stats.ships_left -= 1
        # Update scoreboard.
        sb.prep_ships()
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # pause.
        sleep(0.5)
    else:
        pause_music()
        ai_settings.game_over_sound.play()
        stats.game_active = False
        pygame.mouse.set_visible(True)
    
def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
            break
    
def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """
    Check if the fleet is at an edge,
    Update the postions of all aliens in the fleet."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
        
    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)
    
def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
        
def save_high_score(stats):
    """save high score to txt file."""
    file = open('high_score.txt', "w")
    file.write(str(stats.high_score))
    file.close()
    
def play_music():
    """play background music"""
    pygame.mixer.music.load('music/POL-star-way-short.wav')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    
def pause_music():
    """pause background music"""
    pygame.mixer.music.fadeout(500)
    