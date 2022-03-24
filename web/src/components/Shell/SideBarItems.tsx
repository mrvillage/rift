import SideBarItem from "./SideBarItem";
import { Icon } from "../../utils";

const items = [
  {
    icon: <Icon.Home size={16} />,
    color: "blue",
    label: "Home",
    path: "/home",
  },
  {
    icon: <Icon.Book size={16} />,
    color: "teal",
    label: "Documentation",
    path: "/docs",
    subitems: [
      {
        label: "Getting Started",
        path: "/docs/guides/getting-started",
      },
      { label: "Reference", path: "/docs/reference" },
      { label: "Topics", path: "/docs/topics" },
      { label: "Guides", path: "/docs/guides" },
    ],
  },
  {
    icon: <Icon.Settings size={16} />,
    color: "violet",
    label: "Server Settings",
    path: "/settings",
  },
  {
    icon: <Icon.Settings size={16} />,
    color: "pink",
    label: "Alliance Settings",
    path: "/alliance/settings",
  },
];

const SideBarItems = () => (
  <>
    {items.map((item) => (
      <SideBarItem {...item} key={item.label} />
    ))}
  </>
);

export default SideBarItems;
