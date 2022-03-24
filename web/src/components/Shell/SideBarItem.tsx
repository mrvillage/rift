import {
  Collapse,
  Group,
  Text,
  ThemeIcon,
  UnstyledButton,
} from "@mantine/core";
import { useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import SideBarSubItem, { SideBarSubItemProps } from "./SideBarSubItem";

interface SideBarItemProps {
  icon: React.ReactNode;
  color: string;
  label: string;
  path?: string;
  subitems?: SideBarSubItemProps[];
}

const SideBarItem = ({
  icon,
  color,
  label,
  path,
  subitems,
}: SideBarItemProps) => {
  const [opened, setOpened] = useState(false);
  const navigate = useNavigate();
  return (
    <>
      <UnstyledButton
        sx={(theme) => {
          return {
            display: "block",
            width: "100%",
            padding: theme.spacing.sm,
            borderRadius: theme.radius.sm,
            color: theme.colors.dark[0],

            "&:hover": {
              backgroundColor: theme.colors.dark[6],
            },
          };
        }}
        onClick={() => {
          setOpened(!opened);
          if (path) {
            navigate(path);
          }
        }}
      >
        <Group>
          <ThemeIcon color={color} variant="light">
            {icon}
          </ThemeIcon>
          <Text size="sm">{label}</Text>
        </Group>
      </UnstyledButton>
      <Collapse in={opened}>
        {subitems?.map((subitem) => (
          <SideBarSubItem {...subitem} key={subitem.label} />
        ))}
      </Collapse>
    </>
  );
};

export default SideBarItem;
