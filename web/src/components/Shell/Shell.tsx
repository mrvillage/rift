import { AppShell } from "@mantine/core";
import { useState } from "react";
import SideBar from "./SideBar";
import TopBar from "./TopBar";

interface ShellProps {
  children: React.ReactNode;
}

const Shell = ({ children }: ShellProps) => {
  const [opened, setOpened] = useState(true);
  return (
    <AppShell
      padding="md"
      fixed
      navbarOffsetBreakpoint="sm"
      navbar={<SideBar opened={opened} />}
      header={<TopBar opened={opened} setOpened={setOpened} />}
    >
      {children}
    </AppShell>
  );
};

export default Shell;
