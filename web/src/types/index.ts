import { SupabaseClient } from "@supabase/supabase-js";
export interface State {
  supabase: SupabaseState;
  members: MembersState;
}

export interface SupabaseState {
  supabase: SupabaseClient;
}

export interface MembersState {
  members: Member[];
  currentGuildID: number | null;
  userData: DiscordUser;
  userLink: UserLink;
  userLinked: boolean;
}

export interface SaveState {
  saved: boolean;
}

export interface SideBarItem {
  name: string;
  icon: string;
  path: string;
}
export interface SideBarGroup {
  name: string;
  icon: string;
  path: string;
  items: SideBarItem[];
}
export interface Guild {
  id: number;
  name: string;
  icon_url: string;
  owner_id: number;
}

export interface GuildItem {
  label: string;
  value: number;
}

export interface Member {
  id: number;
  guild: Guild;
  permissions: number;
}

export interface DiscordUser {
  id: number;
  name: string;
  discriminator: string;
  bot: boolean;
  display_avatar_url: string;
}

export interface UserLink {
  user_: number;
  nation: number;
  uuid: string;
}
