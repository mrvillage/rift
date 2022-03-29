import { ActionIcon, Tooltip, useMantineTheme } from "@mantine/core";
import { useMediaQuery } from "@mantine/hooks";
import { themePick } from "../../utils";

interface TopActionIconProps {
  label: string;
  href?: string;
  onClick?: () => void;
  children: React.ReactNode;
}

const TopActionIcon = ({
  label,
  href,
  onClick,
  children,
}: TopActionIconProps) => {
  const theme = useMantineTheme();
  const mobile = useMediaQuery(`(max-width: ${theme.breakpoints.sm}px)`);
  if (href) {
    return (
      <Tooltip label={label} openDelay={500} disabled={mobile}>
        <ActionIcon
          variant="default"
          size={30}
          onClick={() => (window.location.href = href)}
        >
          {children}
        </ActionIcon>
      </Tooltip>
    );
  }
  return (
    <Tooltip label={label} openDelay={500} disabled={mobile}>
      <ActionIcon variant="default" onClick={onClick} size={30}>
        {children}
      </ActionIcon>
    </Tooltip>
  );
};

export default TopActionIcon;
