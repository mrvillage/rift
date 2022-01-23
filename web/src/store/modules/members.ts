import { Member, Guild, MembersState, DiscordUser, UserLink } from "@/types";

const getGuilds = (state: MembersState): Array<Guild> => {
  const guilds = [];
  for (const member of state.members) {
    guilds.push(member.guild);
  }
  return guilds;
};

const state = (): MembersState => ({
  members: [] as Member[],
  currentGuildID: null,
  userData: {} as DiscordUser,
  userLink: {} as UserLink,
  userLinked: false,
});

const getters = {
  getGuilds,
  getCurrentGuild: (state: MembersState): Guild | null => {
    const guilds = [];
    for (const member of state.members) {
      guilds.push(member.guild);
    }
    const val = guilds.find((guild) => guild.id === state.currentGuildID);
    if (val === undefined) {
      return null;
    } else {
      return val;
    }
  },
  getUserData: (state: MembersState): DiscordUser => {
    return state.userData;
  },
  getUserLink: (state: MembersState): UserLink => {
    return state.userLink;
  },
  isUserLinked: (state: MembersState): boolean => {
    return state.userLinked;
  },
};

const actions = {};

const mutations = {
  setCurrentGuildID(state: MembersState, id: number): void {
    state.currentGuildID = id;
  },
  clearMembers(state: MembersState): void {
    state.members = [];
  },
  setMembers(state: MembersState, members: Member[]): void {
    state.members = members;
  },
  setUserData: (state: MembersState, userData: DiscordUser): void => {
    state.userData = userData;
  },
  setUserLink: (state: MembersState, userLink: UserLink): void => {
    state.userLink = userLink;
    state.userLinked = !!userLink.nation;
  },
};

export default {
  state,
  getters,
  actions,
  mutations,
};
