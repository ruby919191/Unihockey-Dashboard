from src.data_loader import get_all_games
from src.utils.filters import apply_filters

def load_and_filter_data():
    all_df = get_all_games()
    df, ausgewaehlte_saisons, selected_game, selected_season, direct_link_mode = apply_filters(all_df)
    return all_df, df, ausgewaehlte_saisons, selected_game, selected_season, direct_link_mode
